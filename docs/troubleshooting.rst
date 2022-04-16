Troubleshooting
===============

This page contains tips and advice about some common errors and problems encountered
with django-jsonform.


Schema and data structure do not match
--------------------------------------

This error occurs when the schema doesn't match the data structure of the JSON.

Some possible causes of this error:


1. **Changing schema for a field**

   If you've changed the schema for an existing field, then the current JSON
   data saved in that field would not match the new schema. So, you'll also need
   to "migrate" the old JSON data to fit the newly written schema.
   Currently, there is no automatic mechanism for migrating JSON data when the schema changes.
   You'll have to do this manually from a Django shell.

2. **Defining schema for existing data**

   If you're defining a schema for existing data, please ensure that the data
   conforms to the schema.
   If the data is too complex and unstructured, it might be difficult to write
   a schema for that. In that case, you should first try to simplify the data.