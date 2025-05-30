from __future__ import annotations

import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field, StrictInt, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class ExperimentStatus(BaseModel):
    """
    ExperimentStatus
    """  # noqa: E501
    experiment_id: Optional[StrictStr] = Field(default=None, alias="experimentId")
    status: Optional[StrictStr] = None
    progress: Optional[StrictInt] = Field(default=None, description="Progress percentage (0-100)")
    __properties: ClassVar[List[str]] = ["experimentId", "status", "progress"]

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
        """Create an instance of ExperimentStatus from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of ExperimentStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {"experimentId": obj.get("experimentId"), "status": obj.get("status"), "progress": obj.get("progress")})
        return _obj
