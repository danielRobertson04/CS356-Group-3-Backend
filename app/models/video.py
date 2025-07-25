from __future__ import annotations

import json
import pprint
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, StrictInt, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Video(BaseModel):
    """
    Video
    """  # noqa: E501
    id: Optional[StrictStr] = None
    title: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    bitDepth: Optional[StrictInt] = None
    path: Optional[StrictStr] = None
    format: Optional[StrictStr] = None
    frameRate: Optional[StrictInt] = Field(default=None, alias="frameRate")
    resolution: Optional[StrictStr] = None
    createdDate: Optional[StrictStr] = Field(default=None, alias="createdDate")
    lastUpdatedBy: Optional[StrictStr] = Field(default=None, alias="lastUpdatedBy")
    __properties: ClassVar[List[str]] = ["id", "title", "description", "bitDepth", "path", "format", "frameRate", "resolution",
                                         "createdDate", "lastUpdatedBy"]

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
        """Create an instance of Video from a JSON string"""
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
        """Create an instance of Video from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({"id": obj.get("id"), "title": obj.get("title"),
                                   "description": obj.get("description"), "bitDepth": obj.get("bitDepth"), "path": obj.get("path"),
                                   "format": obj.get("format"),
                                   "frameRate": obj.get("frameRate"), "resolution": obj.get("resolution"),
                                   "createdDate": obj.get("createdDate"), "lastUpdatedBy": obj.get("lastUpdatedBy")})
        return _obj
