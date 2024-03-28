from __future__ import annotations

import dataclasses
from typing import Type

from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses_jsonschema.type_defs import JsonDict


def json_schema_array(dataclass_cls: Type[JsonSchemaMixin]) -> JsonDict:
    """Get JSON schema representing an array of `dataclass_cls`."""
    WrapperDataClass = type("WrapperDataClass", (JsonSchemaMixin,), {})
    WrapperDataClass.__annotations__["item"] = dataclass_cls
    WrapperDataClass = dataclasses.dataclass(WrapperDataClass)

    schema: JsonDict = WrapperDataClass.json_schema()  # type: ignore

    schema["type"] = "array"
    schema["description"] = f"An array of {dataclass_cls.__name__} objects."
    del schema["required"]
    schema["items"] = schema["properties"]["item"]
    del schema["properties"]

    return schema
