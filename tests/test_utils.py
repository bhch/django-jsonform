from unittest import TestCase
from django_jsonform.utils import (normalize_schema, join_coords, split_coords,
    ErrorMap)
from django_jsonform.constants import JOIN_SYMBOL


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


class TestJoinCoordsFunction(TestCase):
    """Tests for join_coords function"""

    def test_with_one_coord(self):
        self.assertEqual('0', join_coords('0'))

    def test_with_accepts_integers(self):
        self.assertEqual('0', join_coords(0))

    def test_with_multiple_arguments(self):
        self.assertEqual('0%sname' % JOIN_SYMBOL, join_coords(0, 'name'))

    def test_strips_extra_join_symbol(self):
        self.assertEqual(
            '0%sname' % JOIN_SYMBOL,
            join_coords(0, 'name', JOIN_SYMBOL)
        )


class TestSplitCoordsFunction(TestCase):
    """Tests for split_coords function"""

    def test_splits_at_join_symbol(self):
        self.assertEqual(split_coords('a%sb' % JOIN_SYMBOL), ['a', 'b'])


class TestErrorMapClass(TestCase):
    """Tests for ErrorMap class"""

    def test_set_method(self):
        error_map = ErrorMap()
        error_map.set(coords=[0, 'name'], msg='Error')
        self.assertEqual(error_map, {join_coords(0, 'name'): ['Error']})

    def test_append_method(self):
        error_map = ErrorMap()
        
        # 1. append must add a new key if not present
        error_map.append(coords=[0, 'name'], msg='Error 1')
        self.assertEqual(error_map, {join_coords(0, 'name'): ['Error 1']})

        # 2. append must add a new key if not present
        error_map.append(coords=[0, 'name'], msg='Error 2')
        self.assertEqual(
            error_map, 
            {join_coords(0, 'name'): ['Error 1', 'Error 2']}
        )
