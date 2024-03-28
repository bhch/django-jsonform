from __future__ import annotations

import json
from typing import Optional

from django_jsonform.contrib.dataclasses.typedefs import SerializableValue
from django_jsonform.forms.fields import JSONFormField


class DataclassJSONFormField(JSONFormField):
    def prepare_value(self, value: SerializableValue) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, list):
            return json.dumps(
                [x if isinstance(x, dict) else x.to_dict(validate=False) for x in value]
            )
        return json.dumps(
            value if isinstance(value, dict) else value.to_dict(validate=False)
        )
