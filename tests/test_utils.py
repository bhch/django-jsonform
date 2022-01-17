from unittest import TestCase
from django_jsonform.utils import normalize_schema


class TestNormalizeSchemaFunction(TestCase):
    """Tests for utils.normalize_schema function"""

    def test_normalized_schema_is_same(self):
        """Normalized schema must be the same as input schema
        if there are no python objects in the schema.
        """
        schema = {
            'type': 'dict',
            'keys': {
                'name': {
                    'type': 'string',
                },
                'wishlist': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                    }
                }
            }
        }

        self.assertEqual(schema, normalize_schema(schema))
