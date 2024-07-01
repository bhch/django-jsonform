import json
import django
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django_jsonform.utils import _get_django_version

django_major, django_minor = _get_django_version()

if django_major > 3 or (django_major == 3 and django_minor >= 1):
    # Django >= 3.1
    from django.forms import JSONField as DjangoJSONFormField
else:
    # Django < 3.1
    if 'postgres' in settings.DATABASES['default']['ENGINE']:
        from django.contrib.postgres.forms import JSONField as DjangoJSONFormField
    else:
        from django_jsonform.forms.compat import JSONFormField as DjangoJSONFormField

try:
    from django.contrib.postgres.forms import SimpleArrayField
except ImportError:
    class SimpleArrayField:
        mock_field = True

from django_jsonform.widgets import JSONFormWidget

from django.forms.widgets import TextInput
from django_jsonform.validators import JSONSchemaValidator
from django_jsonform.exceptions import JSONSchemaValidationError


class JSONFormField(DjangoJSONFormField):
    def __init__(
        self, *, schema=None, encoder=None, decoder=None, model_name='',
        file_handler='',
        **kwargs
    ):
        self.file_handler = file_handler
        if not kwargs.get('widget'):
            kwargs['widget'] = JSONFormWidget(schema=schema, model_name=model_name, file_handler=file_handler)

        self.widget = kwargs['widget']

        super().__init__(**kwargs)

    def validate(self, value):
        super().validate(value)
        validator = JSONSchemaValidator(schema=self.widget.get_schema())
        try:
            validator(value)
        except JSONSchemaValidationError as e:
            self.add_error(e.error_map)
            raise

    def run_validators(self, value):
        if value in self.empty_values:
            return
        errors = []
        for v in self.validators:
            try:
                v(value)
            except (JSONSchemaValidationError, ValidationError) as e:
                if hasattr(e, 'error_map'):
                    self.add_error(e.error_map)

                if hasattr(e, 'code') and e.code in self.error_messages:
                    e.message = self.error_messages[e.code]
                errors.extend(e.error_list)
        if errors:
            raise ValidationError(errors)

    def add_error(self, error_map):
        self.widget.add_error(error_map)


class ArrayFormField(SimpleArrayField):
    def __init__(self, base_field, **kwargs):
        if hasattr(SimpleArrayField, 'mock_field'):
            raise ImproperlyConfigured('ArrayField requires psycopg2 to be installed.')

        self.base_field = base_field
        self.max_items = kwargs.get('max_length', kwargs.get('size', None))
        self.min_items = kwargs.get('min_length')

        self.nested = kwargs.pop('nested', False)

        if not self.nested:
            self.widget = JSONFormWidget(schema=self.get_schema())
        else:
            self.widget = TextInput

        if not kwargs.get('widget'):
            kwargs['widget'] = self.widget

        super().__init__(base_field, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, list):
            return json.dumps(value, cls=DjangoJSONEncoder)
        return value

    def to_python(self, value):
        if isinstance(value, str):
            value = json.loads(value)
        return super().to_python(value)

    def get_schema(self):
        schema = {'type': 'array'}

        if isinstance(self.base_field, ArrayFormField):
            items = self.base_field.get_schema()
        elif isinstance(self.base_field, django.forms.IntegerField):
            items = {'type': 'number'}
        elif isinstance(self.base_field, JSONFormField):
            items = self.base_field.widget.get_schema()
        else:
            items = {'type': 'string'}
            if isinstance(self.base_field, django.forms.URLField):
                items['format'] = 'uri-reference'

        schema['items'] = items

        if self.max_items:
            schema['max_items'] = self.max_items
        if self.min_items:
            schema['min_items'] = self.min_items

        return schema
