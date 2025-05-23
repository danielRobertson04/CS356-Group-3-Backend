from typing import Optional

from fastapi import Body
from pydantic import Field, StrictStr
from typing_extensions import Annotated

from app.models.experiment import Experiment
from app.models.experiment_input import ExperimentInput
from app.models.experiment_status import ExperimentStatus
from app.services.experiments import ExperimentsService

from fastapi import APIRouter
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.models.error import Error

router = APIRouter()


@router.post("/experiments", responses={200: {"model": Experiment, "description": "Successful operation"},
                                        400: {"description": "Invalid input"},
                                        422: {"description": "Validation exception"},
                                        200: {"model": Error, "description": "Unexpected error"}, },
             tags=["experiments"], summary="Create a new experiment.", response_model_by_alias=True, )
async def create_experiment(experiment_input: Annotated[
    Optional[ExperimentInput], Field(description="Experiment object that needs to be added to the store")] = Body(None,
                                                                                                                  description="Experiment object that needs to be added to the store"),
                            db: AsyncSession = Depends(get_db)) -> Experiment:
    """Create a new experiment under a given user."""
    return await ExperimentsService().create_experiment(experiment_input, db)


@router.delete("/experiments/{experiment_id}",
               responses={200: {"description": "Experiment deleted"}, 400: {"description": "Invalid experiment value"},
                          200: {"model": Error, "description": "Unexpected error"}, }, tags=["experiments"],
               summary="Delete an experiment.", response_model_by_alias=True, )
async def delete_experiment(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."),
        db: AsyncSession = Depends(get_db)) -> None:
    """Delete an experiment."""
    return await ExperimentsService().delete_experiment(experiment_id, db)


@router.get("/experiments/{experiment_id}",
            responses={200: {"model": Experiment, "description": "Successful operation"},
                       400: {"description": "Invalid status value"},
                       200: {"model": Error, "description": "Unexpected error"}, },
            tags=["experiments"], summary="Get experiment by ID.", response_model_by_alias=True, )
async def get_experiment(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."),
        db: AsyncSession = Depends(get_db)) -> Experiment:
    """Get full details of an experiment by its unique ID."""
    return await ExperimentsService().get_experiment(experiment_id, db)


@router.get("/experiments/{experiment_id}/status",
            responses={200: {"model": ExperimentStatus, "description": "Experiment status retrieved successfully."},
                       404: {"model": Error, "description": "Experiment not found."},
                       200: {"model": Error, "description": "Unexpected error while retrieving experiment status."}, },
            tags=["experiments"], summary="Get experiment status", response_model_by_alias=True, )
async def get_experiment_status(
        experiment_id: Annotated[StrictStr, Field(description="Unique ID to identify the experiment.")] = Path(...,
                                                                                                               description="Unique ID to identify the experiment."),
        db: AsyncSession = Depends(get_db)) -> ExperimentStatus:
    """Retrieve the current status and progress of an experiment."""
    return await ExperimentsService().get_experiment_status(experiment_id, db)


@router.get("/experiments", responses={200: {"model": Experiment, "description": "Successful operation"},
                                       400: {"description": "Invalid request"},
                                       422: {"description": "Validation exception"},
                                       200: {"model": Error, "description": "Unexpected error"}, },
            tags=["experiments"], summary="List experiments.", response_model_by_alias=True, )
async def get_experiments(db: AsyncSession = Depends(get_db)) -> Experiment:
    """List experiments for a given user."""
    return await ExperimentsService().get_experiments("1", db)


@router.put("/experiments/{experiment_id}",
            responses={200: {"description": "successful operation"}, 400: {"description": "bad request"},
                       404: {"description": "experiment not found"},
                       200: {"model": Error, "description": "Unexpected error"}, }, tags=["experiments"],
            summary="Update an experiment.", response_model_by_alias=True, )
async def update_experiment(
        experiment_id: Annotated[StrictStr, Field(description="ID to uniquely identify an experiment.")] = Path(...,
                                                                                                                description="ID to uniquely identify an experiment."),
        experiment_input: Annotated[Optional[ExperimentInput], Field(
            description="Experiment object that needs to be added to the store")] = Body(None,
                                                                                         description="Experiment object that needs to be added to the store"),
        db: AsyncSession = Depends(get_db)) -> Experiment:
    """This can only be done by the user who owns the experiment."""
    return await ExperimentsService().update_experiment("1" ,experiment_id, experiment_input, db)
