import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
from django_jsonform.exceptions import JSONSchemaValidationError
from django_jsonform.utils import normalize_keyword, join_coords, ErrorMap
from django_jsonform.constants import JOIN_SYMBOL


@deconstructible
class JSONSchemaValidator:
    def __init__(self, schema):
        self.schema = schema
        self.error_map = ErrorMap()

    def __call__(self, value):
        # reset error_map so that this validator
        # can be reused for the same schema
        self.error_map = ErrorMap()

        schema_type = normalize_keyword(self.schema['type'])

        if schema_type == 'array':
            self.validate_array(self.schema, value, '')
        elif schema_type == 'object':
            self.validate_object(self.schema, value, '')
        else:
            raise JSONSchemaValidationError(
                gettext('Outermost schema type must be either "array" (list) '
                    'or "object" (dict)'
                )
            )

        if self.error_map:
            raise JSONSchemaValidationError(
                gettext('Please correct the errors below.'),
                error_map=self.error_map
            )

    def join_coords(self, *args):
        return join_coords(*args)

    def add_error(self, key, msg):
        if key not in self.error_map:
            self.error_map.set(coords=[key], msg=msg)
        else:
            self.error_map.append(coords=[key], msg=msg)

    def get_validator(self, schema_type):
        return getattr(self, 'validate_%s' % schema_type, None)

    def get_ref(self, ref):
        ref_schema = self.schema
        tokens = ref.split('/')

        for token in tokens:
            if token == '#':
                continue
            else:
                # :TODO: handle KeyError and raise a custom exception
                ref_schema = ref_schema[token]

        return ref_schema

    def get_date(self, value):
        """Returns datetime.date object for the given ``value``.
        Returns None if unable to parse.

        The value must be in YYYY-MM-DD format.
        """
        try:
            return timezone.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return None

    def get_time(self, value):
        """Returns datetime.time object for the given ``value``.
        Returns None if unable to parse.

        The value must be in HH:MM:SS or HH:MM format.
        """
        for format_ in ['%H:%M', '%H:%M:%S']:
            try:
                return timezone.datetime.strptime(value, format_).time()
            except ValueError:
                continue

        return None

    def get_datetime(self, value):
        """Returns datetime.datetime object for the given ``value``.
        Returns None if unable to parse.

        The value must be in ISO format.
        """
        try:
            return timezone.datetime.fromisoformat(value)
        except ValueError:
            return None

    def get_choice_values(self, choices):
        """Returns values for given choices.

        Useful for extracting choice values for object choices.
        """
        values = []
        for choice in choices:
            if isinstance(choice, dict):
                choice = choice.get('value', '')
            values.append(choice)
        return values

    def validate_array(self, schema, data, coords):
        if not isinstance(data, list):
            data_type = type(data).__name__
            data_type_norm = normalize_keyword(data_type)
            raise JSONSchemaValidationError(
                _(
                    'Data sturcture does not match schema. '
                    'Expected an array (list) but got %(schema_type)s instead.'
                ),
                params={'schema_type': '%s (%s)' % (data_type_norm, data_type) if data_type_norm else data_type}
            )

        minItems = schema.get('minItems', schema.get('min_items', None))
        maxItems = schema.get('maxItems', schema.get('max_items', None))
        choices = schema['items'].get('choices', schema['items'].get('enum', None))

        if minItems and len(data) < int(minItems):
            self.add_error(coords, 'Minimum %s items required.' % (minItems))

        if maxItems and len(data) > int(maxItems):
            self.add_error(coords, 'Maximum %s items allowed.' % (maxItems))

        if schema.get('uniqueItems'):
            try:
                if len(data) != len(set(data)):
                    self.add_error(coords, 'All items in this list must be unique.')
            except TypeError:
                # TypeError is raised when trying to make a set from unashable types
                # i.e. lists and dicts
                # so we JSON-ify each item to make it a string
                if len(data) != len(set([json.dumps(item) for item in data])): 
                    self.add_error(coords, 'All items in this list must be unique.')

        if choices:
            choice_values = self.get_choice_values(choices)
            for item in data:
                if item not in choice_values:
                    self.add_error(coords, 'Invalid choice %s' % item)
                    break

        next_schema = schema['items']

        if '$ref' in next_schema:
            next_schema = self.get_ref(next_schema['$ref'])

        next_type = normalize_keyword(next_schema['type'])

        next_validator = self.get_validator(next_type)

        if next_validator:
            for index, item in enumerate(data):
                next_validator(next_schema, item, self.join_coords(coords, index))
        else:
            raise JSONSchemaValidationError(
                _('Unsupported type "%(schema_type)s" for array items.'),
                params={'schema_type': next_type}
            )

    def validate_object(self, schema, data, coords):
        if not isinstance(data, dict):
            data_type = type(data).__name__
            data_type_norm = normalize_keyword(data_type)
            raise JSONSchemaValidationError(
                _(
                    'Data sturcture does not match schema. '
                    'Expected an object (dict) but got %(schema_type)s instead.'
                ),
                params={'schema_type': '%s (%s)' % (data_type_norm, data_type) if data_type_norm else data_type}
            )

        schema_keys = schema.get('properties', schema.get('keys')) or {}

        if not schema_keys.keys() <= data.keys():
            # schema keys must be a subset of data keys
            # i.e. data must have all the keys present in schema
            #
            # We don't care if data has extra keys which are not in the
            # schema because we can't know if the user / programmer might have
            # manually injected those keys in the database
            # so we only validate the keys present in the schema
            raise JSONSchemaValidationError(
                _('These fields are missing from the data: %(fields)s'),
                params={'fields': ', '.join(schema_keys.keys() - data.keys())}
            )

        for key in data:
            if key in schema_keys:
                next_schema = schema_keys[key]
            else:
                if 'additionalProperties' not in schema:
                    continue

                next_schema = schema['additionalProperties']

                if next_schema == True:
                    next_schema = {'type': 'string'}

            if '$ref' in next_schema:
                next_schema = self.get_ref(next_schema['$ref'])

            next_type = normalize_keyword(next_schema['type'])

            next_validator = self.get_validator(next_type)

            if next_validator:
                next_validator(next_schema, data[key], self.join_coords(coords, key))
            else:
                raise JSONSchemaValidationError(
                    _('Unsupported type "%(schema_type)s" for object properties (keys).'),
                    params={'schema_type': next_type}
                )

    def validate_string(self, schema, data, coords):
        if isinstance(data, str):
            data = data.strip()

        if schema.get('required') and not data:
            self.add_error(coords, 'This field is required.')
            return

        if not isinstance(data, str):
            self.add_error(coords, 'This value is invalid. Must be a valid string.')
            return

        if not data:
            # data not required and is empty
            return

        if isinstance(schema.get('minLength'), int) and len(data) < int(schema['minLength']):
            self.add_error(coords, 'Minumum length must be %s' % schema['minLength'])

        if isinstance(schema.get('maxLength'), int) and len(data) > int(schema['maxLength']):
            self.add_error(coords, 'Maximum length must be %s' % schema['maxLength'])

        format_ = normalize_keyword(schema.get('format'))

        if format_:
            if format_ == 'email':
                try:
                    validate_email(data)
                except ValidationError:
                    self.add_error(coords, 'Enter a valid email address.')
            elif format_ == 'date':
                if not self.get_date(data):
                    self.add_error(coords, 'Enter a valid date.')
            elif format_ == 'time':
                if not self.get_time(data):
                    self.add_error(coords, 'Enter a valid time.')
            elif format_ == 'date-time':
                if not self.get_datetime(data):
                    self.add_error(coords, 'Enter a valid date and time.')
 
    def validate_boolean(self, schema, data, coords):
        if schema.get('required') and data is None:
            self.add_error(coords, 'This field is required.')
            return

        if not isinstance(data, bool) and data is not None:
            self.add_error(coords, 'Invalid value.')

    def validate_integer(self, schema, data, coords):
        if schema.get('required') and data is None:
            self.add_error(coords, 'This field is required.')
            return

        if data is None:
            # if not required, integer can be None (or null)
            return

        # 1.0 and 1 must be treated equal
        if isinstance(data, float) and data != int(data):
            self.add_error(coords, 'Invalid value. Only integers allowed.')
            return

        self.validate_number(schema, data, coords)

    def validate_number(self, schema, data, coords):
        if schema.get('required') and data is None:
            self.add_error(coords, 'This field is required.')
            return

        if data is None:
            # if not required, number can be None (or null)
            return

        if not isinstance(data, (float, int)) and data is not None:
            self.add_error(coords, 'Invalid value. Only numbers allowed.')
            return

        data = float(data)

        if  isinstance(schema.get('minimum'), (int, float))  and data < float(schema['minimum']):
            self.add_error(coords, 'This value must not be less than %s' % (schema['minimum']))

        if  isinstance(schema.get('maximum'), (int, float)) and data > float(schema['maximum']):
            self.add_error(coords, 'This value must not be greater than %s' % (schema['maximum']))

        if  isinstance(schema.get('exclusiveMinimum'), (int, float)) and data <= float(schema['exclusiveMinimum']):
            self.add_error(coords, 'This value must be greater than %s' % (schema['exclusiveMinimum']))

        if  isinstance(schema.get('exclusiveMaximum'), (int, float)) and data >= float(schema['exclusiveMaximum']):
            self.add_error(coords, 'This value must be less than %s' % (schema['exclusiveMaximum']))

        if isinstance(schema.get('multipleOf'), (int, float)) and ((data * 100) % (schema['multipleOf'] * 100)) / 100:
            self.add_error(coords, 'This value must be a multiple of %s' % (schema['multipleOf']))

    def __eq__(self, other):
        return self.schema == other.schema
