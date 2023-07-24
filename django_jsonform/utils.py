from django.utils.functional import Promise
from django.conf import settings
from django_jsonform.constants import JOIN_SYMBOL


def normalize_schema(schema):
    """Prepares a schema for converting to JSON.

    We allow python functions in the schema but they aren't
    JSON serializable. This function transforms the schema to
    make it a valid JSON object.

    Eg: Processing lazy translations, etc.
    """

    if isinstance(schema, dict):
        new_schema = {}
        for key, value in schema.items():
            if isinstance(value, (dict, list)):
                value = normalize_schema(value)
            elif isinstance(value, Promise):
                value = str(value)
            new_schema[key] = value
    elif isinstance(schema, list):
        new_schema = []
        for value in schema:
            if isinstance(value, (dict, list)):
                value = normalize_schema(value)
            elif isinstance(value, Promise):
                value = str(value)
            new_schema.append(value)
    else:
        new_schema = {}

    return new_schema


def normalize_keyword(kw):
    """Converts custom keywords to standard JSON schema keywords"""
    return normalize_keyword.kw_map.get(kw, kw)

normalize_keyword.kw_map = {
    'list': 'array',
    'dict': 'object',
    'keys': 'properties',
    'choices': 'enum',
    'datetime': 'date-time'
}

def get_schema_type(schema):
    """Returns the normalized type of schema.

    Will try to sensibly discern the type if 'type' keyword is not present.

    Will return None on failure to guess.
    """
    typ = schema.get('type', None)

    if isinstance(typ, list):
        typ = typ[0]

    if typ is None:
        if 'properties' in schema or 'keys' in schema:
            # if schema has 'properties' or 'keys' keyword
            # it must be an object
            typ = 'object'
        elif 'items' in schema:
            # if schema as 'items' keyword
            # it must be an array
            typ = 'array'

    return normalize_keyword(typ)


def get_setting(name, default=None):
    """Returns settings nested inside DJANGO_JSONFORM main setting variable"""
    if not hasattr(settings, 'DJANGO_JSONFORM'):
        return default

    return settings.DJANGO_JSONFORM.get(name, default)


def join_coords(*coords):
    return JOIN_SYMBOL.join([str(coord) for coord in coords]).strip(JOIN_SYMBOL)


def split_coords(coords):
    return coords.split(JOIN_SYMBOL)


class ErrorMap(dict):
    def set(self, coords, msg):
        key = join_coords(*coords)
        
        if not isinstance(msg, list):
            msg = [msg]

        self[key] = msg

    def append(self, coords, msg):
        key = join_coords(*coords)

        if key not in self:
            self.set(coords, msg)
            return

        if not isinstance(msg, list):
            msg = [msg]

        self[key] = self[key] + msg
