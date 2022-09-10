from unittest import TestCase
from django_jsonform.validators import JSONSchemaValidator
from django_jsonform.exceptions import JSONSchemaValidationError


class TestJSONSchemaValidator(TestCase):
    """Tests for JSONSchemaValidator class"""
    def test_add_error_method(self):
        """JSONSchemaValidator.add_error method must create a list for 
        the given key. All the error messages for thay key must be appended
        to that list.
        """
        validator = JSONSchemaValidator(None)
        validator.add_error('key', 'error message')
        self.assertIsInstance(validator.error_map['key'], list)
        self.assertEqual(validator.error_map['key'][0], 'error message')

    def test_get_ref_method(self):
        pass

    def test_only_array_and_object_allowed_in_top_level(self):
        schema = {'type': 'string'}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, 'value')

        # must pass for array
        schema = {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        }
        validator = JSONSchemaValidator(schema)
        validator([])

        # must pass for object
        schema = {
            'type': 'object',
            'properties': {}
        }
        validator = JSONSchemaValidator(schema)
        validator({})

    def test_validate_array_type(self):
        """Data must be array if schema type is array"""
        # top level array
        schema = {
            'type': 'array', 
            'items': {'type': 'string'}
        }
        wrong_data = {}
        data = []
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

        # nested array
        schema = {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {'type': 'string'}
            }
        }
        wrong_data = [{}]
        data = [[]]
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

    def test_validate_array_min_items(self):
        schema = {
            'type': 'array',
            'items': {'type': 'string'},
            'minItems': 1
        }
        wrong_data = []
        data = ['val']
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

    def test_validate_array_max_items(self):
        schema = {
            'type': 'array',
            'items': {'type': 'string'},
            'maxItems': 1
        }
        wrong_data = ['val', 'val']
        data = ['val']
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

    def test_validate_array_uniqueItems(self):
        # 1. string items
        schema = {
            'type': 'array',
            'items': {'type': 'string'},
            'uniqueItems': True
        }
        wrong_data = ['a', 'b', 'a']
        data = ['a', 'b', 'c']
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

        # 2. dict items
        schema = {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'string'}
                }
            },
            'uniqueItems': True
        }
        wrong_data = [{'a': '1'}, {'a': '1'}]
        data = [{'a': '1'}, {'a': '2'}]
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

        # 3. list items
        schema = {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {'type': 'string'}
            },
            'uniqueItems': True
        }
        wrong_data = [['a', 'b'], ['a', 'b']]
        data_1 = [['a', 'b'], ['a', 'c']]
        data_2 = [['a', 'b'], ['b', 'a']]
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1) # must pass
        validator(data_2) # must pass

    def test_validate_array_choices(self):
        schema = {
            'type': 'array',
            'items': {'type': 'string', 'choices': ['1', '2', '3']}
        }
        wrong_data = ['x']
        data = ['1']
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

    def test_validate_object_type(self):
        """Data must be object if schema type is object"""
        # top level object
        schema = {
            'type': 'object', 
            'properties': {}
        }
        wrong_data = []
        data = {}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

        # nested object
        schema = {
            'type': 'object',
            'properties': {
                'x': {
                    'type': 'object',
                    'properties': {}
                }
            }
        }
        wrong_data = {'x': []}
        data = {'x': {}}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data) # must pass

    def test_data_object_has_the_keys_that_are_in_schema(self):
        """Data must have all the keys declared in the schema.
        It may also have extra keys not present in the schema.
        """
        schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'type': 'string'}
            }
        }
        wrong_data = {'a': ''} # some meys missing
        data_1 = {'a': '', 'b': ''} # exact keys
        data_2 = {'a': '', 'b': '', 'c': ''} # extra keys
        
        validator = JSONSchemaValidator(schema)
        
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1) # must pass
        validator(data_2) # must pass

    def test_additionalProperties_type(self):
        schema = {
            'type': 'object',
            'properties': {'a': {'type': 'string'}},
            'additionalProperties': {'type': 'integer'}
        }
        wrong_data = {'a': '', 'b': '1'}
        data = {'a': '', 'b': 1}

        validator = JSONSchemaValidator(schema)

        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)

        # if additionalProperties is "True",
        # it must be interpreted as string type
        schema = {
            'type': 'object',
            'properties': {'a': {'type': 'string'}},
            'additionalProperties': True
        }
        wrong_data = {'a': '', 'b': 1}
        data = {'a': '', 'b': '1'}

        validator = JSONSchemaValidator(schema)
        
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)

    def test_array_items_ref(self):
        # when array.items is a reference
        schema = {
            'type': 'array', 
            'items': {'$ref': '#/$defs/itemsRef'},
            '$defs': {
                'itemsRef': {
                    'type': 'integer'
                }
            }
        }
        wrong_data = ['1']
        data = [1]
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)

    def test_object_properties_ref(self):
        # when a property is a reference
        schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'$ref': '#/properties/a'},
            }
        }
        wrong_data_1 = {'a': '1'}
        wrong_data_2 = {'a': '1', 'b': 2}
        data = {'a': '1', 'b': '2'}

        validator = JSONSchemaValidator(schema)

        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data)

    def test_additionalProperties_ref(self):
        # when additionalProperties is a reference
        schema = {
            'type': 'object',
            'properties': {'a': {'type': 'string'}},
            'additionalProperties': {'$ref': '#/properties/a'}
        }
        wrong_data = {'a': '1', 'b': 2}
        data = {'a': '1', 'b': '2'}

        validator = JSONSchemaValidator(schema)

        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)

    def test_validate_string_method(self):
        schema = {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'string',
                    'required': True,
                    'minLength': 3,
                    'maxLength': 5
                }
            }
        }
        
        validator = JSONSchemaValidator(schema)

        # 1. test required
        wrong_data = {'a': ''}
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)

        # 2. test type
        wrong_data = {'a': 123}
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)

        # 3. test minLength
        wrong_data = {'a': '12'}
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        
        # 4. test maxLength
        wrong_data = {'a': '123456'}
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)

        # correct data
        data = {'a': '123'}
        validator(data)

        # 5. test maxLength when zero
        schema['properties']['a']['maxLength'] = 0
        wrong_data = {'a': '123456'}
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)

    def test_validate_string_formats(self):
        # 1. email
        schema = {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'string',
                    'format': 'email'
                }
            }
        }
        wrong_data = {'a': '1'}
        data = {'a': 'test@example.com'}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)

        # 2. date
        schema['properties']['a']['format'] = 'date'
        wrong_data = {'a': '2022-100-100'}
        data = {'a': '2022-09-01'}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)

        # 3. time
        schema['properties']['a']['format'] = 'time'
        wrong_data = {'a': '12 pm'}
        data_1 = {'a': '12:10'}
        data_2 = {'a': '12:10:08'}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)

        # 4. date-time
        schema['properties']['a']['format'] = 'date-time'
        wrong_data = {'a': '5 Sept, 2022'}
        data_1 = {'a': '2022-09-05'}
        data_2 = {'a': '2022-09-05T06:53:19.119527'}
        data_3 = {'a': '2022-09-05T06:53:19.119527+00:00'}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)
        validator(data_3)

    def test_validate_boolean_method(self):
        # 1. type (either bool or None)
        schema = {
            'type': 'object',
            'properties': {'a': {'type': 'boolean'}}
        }
        wrong_data = {'a': 1}
        data_1 = {'a': True}
        data_2 = {'a': False}
        data_3 = {'a': None}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)
        validator(data_3)

        # 2. required (only bool)
        schema['properties']['a']['required'] = True
        wrong_data = {'a': None}
        data_1 = {'a': True}
        data_2 = {'a': False}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)

    def test_validate_integer_method(self):
        # 1. type (either int or None)
        schema = {
            'type': 'object',
            'properties': {'a': {'type': 'integer'}}
        }
        wrong_data_1 = {'a': '1'}
        wrong_data_2 = {'a': 1.1}
        data_1 = {'a': 1}
        data_2 = {'a': 0}
        data_3 = {'a': -1}
        data_4 = {'a': None}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data_1)
        validator(data_2)
        validator(data_3)
        validator(data_4)

        # 2. required (only int)
        schema['properties']['a']['required'] = True
        wrong_data = {'a': None}
        data = {'a': 1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)

        # 3. 1.0 must be treated as 1
        data = {'a': 1.0}
        validator(data)

        # 4. minimum & maximum
        schema['properties']['a']['minimum'] = 2
        schema['properties']['a']['maximum'] = 5
        wrong_data_1 = {'a': 1}
        wrong_data_2 = {'a': 6}
        data_1 = {'a': 2}
        data_2 = {'a': 3}
        data_3 = {'a': 5}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data_1)
        validator(data_2)
        validator(data_3)

        # 5. minimum when zero
        del schema['properties']['a']['maximum'];
        schema['properties']['a']['minimum'] = 0
        wrong_data = {'a': -1}
        data_1 = {'a': 0}
        data_2 = {'a': 1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)

        # 6. maximum when zero
        schema['properties']['a']['maximum'] = 0
        del schema['properties']['a']['minimum']
        wrong_data = {'a': 1}
        data_1 = {'a': 0}
        data_2 = {'a': -1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)

        # 7. exclusiveMinimum & exclusiveMaximum
        del schema['properties']['a']['maximum']
        schema['properties']['a']['exclusiveMinimum'] = 2
        schema['properties']['a']['exclusiveMaximum'] = 5
        wrong_data_1 = {'a': 1}
        wrong_data_2 = {'a': 6}
        wrong_data_3 = {'a': 2}
        wrong_data_4 = {'a': 5}
        data_1 = {'a': 3}
        data_2 = {'a': 4}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_3)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_4)
        validator(data_1)
        validator(data_2)

        # 8. exclusiveMinimum when zero
        schema['properties']['a']['exclusiveMinimum'] = 0
        del schema['properties']['a']['exclusiveMaximum']
        wrong_data_1 = {'a': -1}
        wrong_data_2 = {'a': 0}
        data = {'a': 1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data)

        # 9. exclusiveMaximum when zero
        del schema['properties']['a']['exclusiveMinimum']
        schema['properties']['a']['exclusiveMaximum'] = 0
        wrong_data_1 = {'a': 1}
        wrong_data_2 = {'a': 0}
        data = {'a': -1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data)

        # 10. multipleOf
        del schema['properties']['a']['exclusiveMaximum']
        schema['properties']['a']['multipleOf'] = 2
        wrong_data = {'a': 1}
        data = {'a': 4}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)


    def test_validate_number_method(self):
        # 1. type (either float or int or None)
        schema = {
            'type': 'object',
            'properties': {'a': {'type': 'number'}}
        }
        wrong_data = {'a': '1'}
        data_1 = {'a': 1.0}
        data_2 = {'a': 0}
        data_3 = {'a': -1.5}
        data_4 = {'a': None}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)
        validator(data_3)
        validator(data_4)

        # 2. required (float or int)
        schema['properties']['a']['required'] = True
        wrong_data = {'a': None}
        data_1 = {'a': 1.5}
        data_2 = {'a': 1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)

        # 3. minimum & maximum
        schema['properties']['a']['minimum'] = 2.5
        schema['properties']['a']['maximum'] = 5.2
        wrong_data_1 = {'a': 2.4}
        wrong_data_2 = {'a': 5.25}
        data_1 = {'a': 2.5}
        data_2 = {'a': 3.0}
        data_3 = {'a': 5.2}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data_1)
        validator(data_2)
        validator(data_3)

        # 4. minimum when zero
        del schema['properties']['a']['maximum'];
        schema['properties']['a']['minimum'] = 0.0
        wrong_data = {'a': -0.1}
        data_1 = {'a': 0.0}
        data_2 = {'a': 0.1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)

        # 5. maximum when zero
        schema['properties']['a']['maximum'] = 0.0
        del schema['properties']['a']['minimum']
        wrong_data = {'a': 0.1}
        data_1 = {'a': 0.0}
        data_2 = {'a': -0.1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data_1)
        validator(data_2)

        # 6. exclusiveMinimum & exclusiveMaximum
        del schema['properties']['a']['maximum']
        schema['properties']['a']['exclusiveMinimum'] = 2.5
        schema['properties']['a']['exclusiveMaximum'] = 5.2
        wrong_data_1 = {'a': 1.0}
        wrong_data_2 = {'a': 6.0}
        wrong_data_3 = {'a': 2.5}
        wrong_data_4 = {'a': 5.2}
        data_1 = {'a': 2.6}
        data_2 = {'a': 5.1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_3)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_4)
        validator(data_1)
        validator(data_2)

        # 7. exclusiveMinimum when zero
        schema['properties']['a']['exclusiveMinimum'] = 0.0
        del schema['properties']['a']['exclusiveMaximum']
        wrong_data_1 = {'a': -0.1}
        wrong_data_2 = {'a': 0.0}
        data = {'a': 0.1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data)

        # 8. exclusiveMaximum when zero
        del schema['properties']['a']['exclusiveMinimum']
        schema['properties']['a']['exclusiveMaximum'] = 0.0
        wrong_data_1 = {'a': 0.1}
        wrong_data_2 = {'a': 0.0}
        data = {'a': -0.1}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_1)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data_2)
        validator(data)

        # 9. multipleOf
        del schema['properties']['a']['exclusiveMaximum']
        schema['properties']['a']['multipleOf'] = 0.2
        wrong_data = {'a': 4.15}
        data = {'a': 4.0}
        validator = JSONSchemaValidator(schema)
        self.assertRaises(JSONSchemaValidationError, validator, wrong_data)
        validator(data)
