Quickstart
==========

``django-jsonform`` allows you to edit JSON data by supplying a *schema* for the
data structure.

Shopping list
-------------

Suppose we want to create a model for saving shopping lists. A typical shopping
list looks like this: ``['eggs', 'milk', 'juice']``. It is basically a
**list of strings**.

Sample model
------------

``django-jsonform`` provides a custom :class:`~django_jsonform.models.fields.JSONField`
for your convenience. You can also use the :class:`widget <django_jsonform.widgets.JSONFormWidget>`
but it requires a little more work to set up.

Here's a model with sample schema:

.. code-block:: python

    # models.py

    from django.db import models
    from django_jsonform.models.fields import JSONField


    class ShoppingList(models.Model):
        ITEMS_SCHEMA = {
            'type': 'array', # a list which will contain the items
            'items': {
                'type': 'string' # items in the array are strings
            }
        }

        items = JSONField(schema=ITEMS_SCHEMA)
        date_created = models.DateTimeField(auto_now_add=True)


Admin
-----

Register your model for the admin site:

.. code-block:: python

    # admin.py

    from django.contrib import admin
    from myapp.models import ShoppingList


    admin.site.register(ShoppingList)


Now go to the admin site and visit the *"Add new"* shopping list page. The form should
look something like this:

.. image:: _static/quickstart.gif
    :alt: Animated screenshot of admin page


Next steps
----------

- The :doc:`User's guide <guide/index>` contains further details about various
  input types, uploading files and other features.
- See :doc:`schema` for a reference on the supported schema.
- See :doc:`fields-and-widgets` for available fields and widgets.
- See :doc:`examples` for sample schemas for declaring complex data structures.