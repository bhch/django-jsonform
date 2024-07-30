from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Type

from django_jsonform.contrib.dataclasses.forms.fields import DataclassJSONFormField
from django_jsonform.contrib.dataclasses.typedefs import DataclassJsonSchema, SerializableValue
from django_jsonform.contrib.dataclasses.utils import json_schema_array
from django_jsonform.exceptions import JSONSchemaValidationError
from django_jsonform.models.fields import JSONField

if TYPE_CHECKING:
    from django.db import models
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.models.expressions import Expression


class DataclassJSONField(JSONField):
    form_class = DataclassJSONFormField

    def __init__(
        self,
        dataclass_cls: Type[DataclassJsonSchema],
        *,
        many: bool = False,
        **kwargs: Any,
    ) -> None:
        self._dataclass_cls = dataclass_cls
        self._many = many
        self._json_schema = (
            json_schema_array(dataclass_cls) if many else dataclass_cls.json_schema()
        )

        super().__init__(schema=self._json_schema, **kwargs)  # type: ignore

    def deconstruct(self) -> Tuple[str, str, List[Any], Dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["dataclass_cls"] = self._dataclass_cls
        kwargs["many"] = self._many
        return name, path, args, kwargs

    def from_db_value(
        self,
        value: Optional[str],
        expression: Expression,
        connection: BaseDatabaseWrapper,
    ) -> SerializableValue:
        if value is None:
            return None
        data = json.loads(value)
        if isinstance(data, list):
            return [self._dataclass_cls.from_dict(x, validate=False) for x in data]
        return self._dataclass_cls.from_dict(data, validate=False)

    def get_prep_value(self, value: SerializableValue) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, list):
            return json.dumps(
                [x if isinstance(x, dict) else x.to_dict(validate=False) for x in value]
            )
        return json.dumps(
            value if isinstance(value, dict) else value.to_dict(validate=False)
        )

    def validate(self, value: SerializableValue, model_instance: models.Model) -> None:
        if value is None:
            if not self.null:
                raise JSONSchemaValidationError("Null value in non-nullable field.")  # type: ignore
            return
        values_to_validate = value if isinstance(value, list) else [value]
        if len(values_to_validate) == 0:
            if not self.blank:
                raise JSONSchemaValidationError("Blank value in non-blank field.")  # type: ignore
            return
        errs: List[str] = []
        for i, val in enumerate(values_to_validate):
            try:
                if isinstance(val, dict):
                    self._dataclass_cls.from_dict(
                        val, validate=True, validate_enums=True
                    )
                else:
                    val.to_dict(validate=True, validate_enums=True)
            except Exception as e:
                errs.append(f"[{i}] {e}")
        if errs:
            raise JSONSchemaValidationError(errs)  # type: ignore
