Using with Postgres ``ArrayField``
==================================

django-jsonform provides a custom :class:`~django_jsonform.models.fields.ArrayField`
class which renders a dynamic form input.

It is a subclass of Django's ``ArrayField`` and the usage api is exactly the same.

.. code-block:: python

    from django_jsonform.models.fields import ArrayField


    class MyModel(models.Model):
        items = ArrayField(models.CharField(max_length=50), size=10)


.. _arrayfield custom schema:

Custom schema for ``ArrayField``
--------------------------------

.. versionadded:: 2.23

Overriding the schema is useful when you want to render custom widgets on the 
browser.

However, it is your responsibility to write the correct schema as mismatches in
data structure may cause validation errors while saving data.

Example:

.. code:: python

    from django_jsonform.models.fields import ArrayField


    class MyModel(...):
        ITEMS_SCHEMA = {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": 50
            },
            "maxItems": 10
        }

        items = ArrayField(models.CharField(max_length=50), size=10, schema=ITEMS_SCHEMA)


.. _arrayfield custom widget:

Overriding the widget for ``ArrayField``
----------------------------------------

.. versionadded:: 2.23

The default widget for the ``ArrayField`` can be overridden to provide custom schema
and do some other stuff.

If you only need to provide custom schema, then it's better to just use the ``schema``
argument as described in the :ref:`previous section <arrayfield custom schema>`.

Overriding the widget for ``ArrayField`` works the same way as for the ``JSONField``.
For usage examples, see: :class:`~django_jsonform.widgets.JSONFormWidget`.
