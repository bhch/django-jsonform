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


Selecting multiple items
------------------------

Currently only one item can be selected. This is because the ``string`` type
can't be a list.

For multiple selections, you should use an ``array``.
