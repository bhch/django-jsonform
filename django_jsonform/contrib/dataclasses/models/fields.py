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


    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Some backends (SQLite at least) extract non-string values in their
        # SQL datatypes.
        if isinstance(expression, KeyTransform) and not isinstance(value, str):
            return value
        try:
            return json.loads(value, cls=self.decoder)
        except json.JSONDecodeError:
            return value

    def get_internal_type(self):
        return "JSONField"

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value, cls=self.encoder)

    def get_transform(self, name):
        transform = super().get_transform(name)
        if transform:
            return transform
        return KeyTransformFactory(name)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            json.dumps(value, cls=self.encoder)
        except TypeError:
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )
