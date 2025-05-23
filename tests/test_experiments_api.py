from fastapi.testclient import TestClient

from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import Any, List, Optional, Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from app.models.error import Error  # noqa: F401
from app.models.experiment import Experiment  # noqa: F401
from app.models.experiment_input import ExperimentInput  # noqa: F401
from app.models.experiment_status import ExperimentStatus  # noqa: F401


def test_create_experiment(client: TestClient):
    """Test case for create_experiment

    Create a new experiment.
    """
    experiment_input = {
        "experimentName": "Streaming Test A",
        "description": "Testing encoding and network parameters",
        "videoSources": ["intro.mp4", "main.mp4"],
        "encodingParameters": {
            "codec": "h265",
            "bitrate": "3000",
            "resolution": "1280x720"
        },
        "networkConditions": {
            "packet_loss": "0.01",
            "delay": "100"
        },
        "metricsRequested": ["latency", "packetLoss", "bitrate"]
    }
    headers = {
    }
    # uncomment below to make a request
    response = client.request(
        "POST",
        "/experiments",
        headers=headers,
        json=experiment_input,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_delete_experiment(client: TestClient):
    """Test case for delete_experiment

    Delete an experiment.
    """

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
        "DELETE",
        "/experiments/{experimentId}".format(experimentId='1'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_get_experiment(client: TestClient):
    """Test case for get_experiment

    Get experiment by ID.
    """

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
        "GET",
        "/experiments/{experimentId}".format(experimentId='1'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_get_experiment_status(client: TestClient):
    """Test case for get_experiment_status

    Get experiment status
    """

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
        "GET",
        "/experiments/{experimentId}/status".format(experimentId='1'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_get_experiments(client: TestClient):
    """Test case for get_experiments

    List experiments.
    """

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
        "GET",
        "/experiments",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_update_experiment(client: TestClient):
    """Test case for update_experiment

    Update an experiment.
    """
    experiment_input = {
        "experimentName": "Streaming Test A",
        "description": "Testing encoding and network parameters",
        "videoSources": ["intro.mp4", "main.mp4"],
        "encodingParameters": {
            "codec": "h265",
            "bitrate": "3000",
            "resolution": "1280x720"
        },
        "networkConditions": {
            "packet_loss": "0.01",
            "delay": "100"
        },
        "metricsRequested": ["latency", "packetLoss", "bitrate"]
    }

    headers = {
    }
    # uncomment below to make a request
    response = client.request(
        "PUT",
        "/experiments/{experimentId}".format(experimentId='experiment_id_example'),
        headers=headers,
        json=experiment_input,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200
