from __future__ import annotations

import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field, StrictStr

from app.models.encoding_parameters import EncodingParameters
from app.models.network_conditions import NetworkConditions

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class ExperimentInput(BaseModel):
    """
    ExperimentInput
    """  # noqa: E501
    experiment_name: StrictStr = Field(alias="experimentName")
    description: Optional[StrictStr] = None
    video_sources: List[StrictStr] = Field(alias="videoSources")
    encoding_parameters: EncodingParameters = Field(alias="encodingParameters")
    network_conditions: NetworkConditions = Field(alias="networkConditions")
    metrics_requested: List[StrictStr] = Field(alias="metricsRequested")
    __properties: ClassVar[List[str]] = ["experimentName", "description", "videoSources", "encodingParameters",
                                         "networkConditions", "metricsRequested"]

    model_config = {"populate_by_name": True, "validate_assignment": True, "protected_namespaces": (), }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ExperimentInput from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(by_alias=True, exclude={}, exclude_none=True, )
        # override the default output from pydantic by calling `to_dict()` of encoding_parameters
        if self.encoding_parameters:
            _dict['encodingParameters'] = self.encoding_parameters.to_dict()
        # override the default output from pydantic by calling `to_dict()` of network_conditions
        if self.network_conditions:
            _dict['networkConditions'] = self.network_conditions.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of ExperimentInput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({"experimentName": obj.get("experimentName"), "description": obj.get("description"),
                                   "videoSources": obj.get("videoSources"),
                                   "encodingParameters": ExperimentInput.from_dict(
                                       obj.get("encodingParameters")) if obj.get(
                                       "encodingParameters") is not None else None,
                                   "networkConditions": ExperimentInput.from_dict(
                                       obj.get("networkConditions")) if obj.get(
                                       "networkConditions") is not None else None,
                                   "metricsRequested": obj.get("metricsRequested")})
        return _obj


# TODO: Rewrite to not use raise_errors
ExperimentInput.model_rebuild(raise_errors=False)
