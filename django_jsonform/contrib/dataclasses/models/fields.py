from typing import Any, Type

from dataclasses_jsonschema import JsonSchemaMixin
from django_jsonform.contrib.dataclasses.models.utils import json_schema_array
from django_jsonform.models.fields import JSONField


class DataclassJSONField(JSONField):
    def __init__(
        self, dataclass_cls: Type[JsonSchemaMixin], *, many: bool = False, **kwargs: Any
    ) -> None:
        self._dataclass_cls = dataclass_cls
        self._many = many
        self._json_schema = (
            json_schema_array(dataclass_cls) if many else dataclass_cls.json_schema()
        )

        super().__init__(schema=self._json_schema, **kwargs)
