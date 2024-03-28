from __future__ import annotations

from typing import List, Optional, Union

from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses_jsonschema.type_defs import JsonDict

DataclassJsonSchema = JsonSchemaMixin
"""TODO: Make this a Protocol or something. Not sure."""


SerializableValue = Optional[
    Union[DataclassJsonSchema, JsonDict, List[Union[DataclassJsonSchema, JsonDict]]]
]
