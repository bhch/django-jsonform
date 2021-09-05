import json
import django
from django.db import models
from django.conf import settings

if django.VERSION[0] >= 3 and django.VERSION[1] >= 1:
    # Django >= 3.1
    from django.forms import JSONField as DjangoJSONFormField
else:
    # Django < 3.1
    if 'postgres' in settings.DATABASES['default']['ENGINE']:
        from django.contrib.postgres.forms import JSONField as DjangoJSONFormField
    else:
        from django_jsonform.forms.compat import JSONFormField as DjangoJSONFormField

from django.contrib.postgres.forms import SimpleArrayField
from django_jsonform.widgets import JSONFormWidget

from django.forms.widgets import TextInput


class JSONFormField(DjangoJSONFormField):
    def __init__(
        self, *, schema=None, encoder=None, decoder=None, model_name='',
        **kwargs
    ):
        self.widget = JSONFormWidget(schema=schema, model_name=model_name)
        kwargs['widget'] = self.widget
        super().__init__(**kwargs)


class ArrayFormField(SimpleArrayField):
    def __init__(self, base_field, **kwargs):
        self.base_field = base_field
        self.max_items = kwargs.get('max_length', kwargs.get('size', None))
        self.min_items = kwargs.get('min_length')

        self.nested = kwargs.pop('nested', False)

        if not self.nested:
            self.widget = JSONFormWidget(schema=self.get_schema())
        else:
            self.widget = TextInput
        kwargs['widget'] = self.widget

        super().__init__(base_field, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, list):
            return json.dumps(value)
        return value

    def to_python(self, value):
        if isinstance(value, str):
            value = json.loads(value)
        return super().to_python(value)

    def get_schema(self):
        schema = {'type': 'array'}

        if isinstance(self.base_field, ArrayFormField):
            items = self.base_field.get_schema()
        elif  isinstance(self.base_field, models.IntegerField):
            items = {'type': 'number'}
        else:
            items = {'type': 'string'}

        schema['items'] = items

        if self.max_items:
            schema['max_items'] = self.max_items
        if self.min_items:
            schema['min_items'] = self.min_items

        return schema