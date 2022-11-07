from __future__ import annotations

import json

from django_jsonform.forms.fields import JSONFormField


class DataclassJSONFormField(JSONFormField):
    def prepare_value(self, value):
        if value is None:
            return None
        if isinstance(value, list):
            return json.dumps([x.to_dict() for x in value])
        return json.dumps(value.to_dict())
