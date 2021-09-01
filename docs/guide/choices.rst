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


Selecting multiple items
------------------------

Currently only one item can be selected. This is because the ``string`` type
can't be an list.

For multiple selections, you should use an ``array``.

