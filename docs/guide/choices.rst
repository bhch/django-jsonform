Choices
======= 

You can specify choices for an input field using the ``choices`` keyword.

Choices can be specified for any type of input - ``string``, ``number``, ``boolean`` etc.


Specifying choices
------------------

.. code-block:: python

    {
        'type': 'string',
        'choices': ['Eggs', 'Milk', 'Juice']
    }


You can also specify a different label for displaying to the user while the
underlying value is different.

.. code-block:: python

    {
        'type': 'string',
        'choices': [
            {'label': 'New York', 'value': 'NY'},
            {'label': 'California', 'value': 'CA'},
            {'label': 'Texas', 'value': 'TX'},
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
