Troubleshooting
===============

This page contains tips and advice about some common errors and problems encountered
with django-jsonform.


Schema and data structure do not match
--------------------------------------

This error occurs when the schema doesn't match the data structure of the JSON.

JSON is a flexible format and it's used for storing data with arbitrary structure.
However, the purpose of a schema is to enforce a structure on the JSON data.

If you're defining a schema for existing data, please ensure that the data
conforms to the schema.

If the data is too complex and unstructured, it might be difficult to write
a schema for that. In that case, you should first try to simplify the data.