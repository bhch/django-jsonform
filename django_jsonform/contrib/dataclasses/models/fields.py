import json
from typing import Any, Type

from dataclasses_jsonschema import JsonSchemaMixin
from django_jsonform.contrib.dataclasses.forms.fields import DataclassJSONFormField
from django_jsonform.contrib.dataclasses.models.utils import json_schema_array
from django_jsonform.models.fields import JSONField


class DataclassJSONField(JSONField):
    form_class = DataclassJSONFormField

    def __init__(
        self, dataclass_cls: Type[JsonSchemaMixin], *, many: bool = False, **kwargs: Any
    ) -> None:
        self._dataclass_cls = dataclass_cls
        self._many = many
        self._json_schema = (
            json_schema_array(dataclass_cls) if many else dataclass_cls.json_schema()
        )

        super().__init__(schema=self._json_schema, **kwargs)

    def from_db_value(self, value, _expression, _connection):
        if value is None:
            return None
        data = json.loads(value)
        if self._many:
            return [self._dataclass_cls.from_dict(x) for x in data]
        return self._dataclass_cls.from_dict(data)

    def get_prep_value(self, value):
        if value is None:
            return None
        if self._many:
            return json.dumps([x.to_dict() for x in value])
        return json.dumps(value.to_dict())

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
