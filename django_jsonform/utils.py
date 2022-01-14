from django.utils.functional import Promise


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
