import json

from app.models.experiment import Experiment


def validate_experiment(db_obj):
    return Experiment.model_validate({
        "id": str(db_obj.id),  # convert int to str if Pydantic expects str
        "experimentName": db_obj.experiment_name,  # match exact Pydantic field name
        "description": db_obj.description,
        "owner_id": db_obj.owner_id,
        "status": db_obj.status,
        "video_sources": json.loads(db_obj.video_sources) if db_obj.video_sources else [],
        "encoding_parameters": json.loads(db_obj.encoding_parameters) if db_obj.encoding_parameters else {},
        "network_conditions": json.loads(db_obj.network_conditions) if db_obj.network_conditions else {},
        "metrics_requested": json.loads(db_obj.metrics_requested) if db_obj.metrics_requested else [],
        "progress": db_obj.progress,
        "created_at": db_obj.created_at.isoformat() if db_obj.created_at else None,
    })