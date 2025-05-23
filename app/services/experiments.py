import json
from typing import Optional, ClassVar, Tuple

from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import Field, StrictStr
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing_extensions import Annotated

from app.database.tables.experiments import Experiment as experiment_table
from app.models.experiment import Experiment
from app.models.experiment_input import ExperimentInput
from app.models.experiment_status import ExperimentStatus
from tests.utility.validation import validate_experiment


class ExperimentsService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ExperimentsService.subclasses = ExperimentsService.subclasses + (cls,)

    async def create_experiment(self, experiment_input: Annotated[
        Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")],
                                db: AsyncSession) -> Experiment:
        # Check if experiment name already exists
        result = await db.execute(
            select(experiment_table).where(or_(experiment_table.experiment_name == experiment_input.experiment_name)))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Experiment name already exists")
        # Create and save experiment
        data = experiment_input.model_dump(exclude_none=True, by_alias=False)
        data["video_sources"] = json.dumps(data["video_sources"])
        data["metrics_requested"] = json.dumps(data["metrics_requested"])
        data["encoding_parameters"] = json.dumps(data["encoding_parameters"])
        data["network_conditions"] = json.dumps(data["network_conditions"])
        data["owner_id"] = "1"  # todo fix
        data["status"] = "created"  # status
        db_obj = experiment_table(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return validate_experiment(db_obj)

    async def delete_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")],
                                db: AsyncSession) -> None:
        result = await db.execute(select(experiment_table).where(experiment_table.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")

        await db.delete(db_obj)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "User deleted"})

    async def get_experiment(self, experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")],
                             db: AsyncSession) -> Experiment:
        result = await db.execute(select(experiment_table).where(experiment_table.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return validate_experiment(db_obj)

    async def get_experiment_status(self, experiment_id: Annotated[
        StrictStr, Field(description="Unique ID to identify the experiment.")],
                                    db: AsyncSession) -> ExperimentStatus:
        result = await db.execute(select(experiment_table).where(experiment_table.id == experiment_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Experiment not found")
        return validate_experiment(db_obj)

    async def get_experiments(self, user_id: Annotated[StrictStr, Field(description="ID to uniquely identify a user.")],
                              db: AsyncSession) -> Experiment:
        result = await db.execute(select(experiment_table).where(experiment_table.owner_id == user_id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="No experiments found for user")
        return validate_experiment(db_obj)

    async def update_experiment(self, user_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify the current user.")], experiment_id: Annotated[
        StrictStr, Field(description="ID to uniquely identify an experiment.")], experiment_input: Annotated[
        Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")],
                                db: AsyncSession) -> Experiment:
        """This can only be done by the user who owns the experiment."""
        result = await db.execute(select(experiment_table).where(experiment_table.id == experiment_id))
        experiment = result.scalars().first()

        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
        if not experiment.owner_id == user_id:
            raise HTTPException(status_code=404, detail="Only the owner of the experiment can update the experiment")
        updates = experiment_input.model_dump(exclude_none=True)

        updates["video_sources"] = json.dumps(updates["video_sources"])
        updates["metrics_requested"] = json.dumps(updates["metrics_requested"])
        updates["encoding_parameters"] = json.dumps(updates["encoding_parameters"])
        updates["network_conditions"] = json.dumps(updates["network_conditions"])
        updates["owner_id"] = "1"  # todo fix
        updates["status"] = json.dumps(experiment.status) # status

        for field, value in updates.items():
            setattr(experiment, field, value)

        db.add(experiment)
        await db.commit()
        await db.refresh(experiment)
        return validate_experiment(experiment)
