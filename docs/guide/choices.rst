Choices
======= 

You can specify choices for an input field using the ``choices`` (or ``enum``) keyword.

Choices can be specified for any type of input - ``string``, ``number``, ``boolean`` etc.

.. versionchanged:: 2.11.0
    Support for ``enum`` keyword was added.

.. versionchanged:: 2.12.0
    ``title`` keyword was added as an alias for the ``label`` keyword.

Specifying choices
------------------

.. code-block:: python

    {
        'type': 'string',
        'choices': ['Eggs', 'Milk', 'Juice'] # you can also use 'enum' keyword
    }


You can also specify a different title for displaying to the user while the
underlying value is different.

.. code-block:: python

    {
        'type': 'string',
        'choices': [
            {'title': 'New York', 'value': 'NY'},
            {'title': 'California', 'value': 'CA'},
            {'title': 'Texas', 'value': 'TX'},
        ]
    }


Customizing the input field
---------------------------

By default, a ``select`` input is rendered for the choices.

You can also use a ``radio`` input using the ``widget`` keyword:

.. code-block:: python

    {
        'type': 'string',
        'choices': ['Eggs', 'Milk', 'Juice'],
        'widget': 'radio'
    }


Multiple selections
-------------------

.. versionadded:: 2.8

For multiple selections, you'll have to use an ``array`` type to hold the selected
values.

To disallow users from selecting the same value multiple times, you can use ``multiselect`` widget.

.. code-block:: python

    {
        'type': 'array',
        'items': {
            'type': 'string',
            'choices': ['Eggs', 'Milk', 'Juice'],
            'widget': 'multiselect'
        }
    }

The ``multiselect`` widget ensures that one value can only be selected once.

Don't use ``multiselect`` widget if you want to let your users select the same value
multiple times.


Dynamic choices
---------------

In some cases, you might want to return choices dynamically, such as by reading
objects from the database.

For that purpose, the ``schema`` can be a callable object:

.. code-block:: python

    def dynamic_schema():
        # here, you can create a schema dynamically
        # such as read data from database and populate choices
        schema = {...}
        return schema


    class MyModel(models.Model):
        items = JSONField(schema=dynamic_schema)


AJAX choices
------------

See :doc:`Autocomplete widget </guide/autocomplete>` for loading choices via AJAX
requests.
