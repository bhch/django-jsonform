Coordinates
===========

*"Coordinates"* are a way to locate a nested item in a data.

Consider the following data—a list of persons:

.. code-block:: python

    data = [
        {
            'name': 'Alice',
            'age': 30,
            'children':[
                {
                    'name': 'Carl',
                    'age': 8
                }
            ]
        },

        {
            'name': 'Bob',
            'age': '40',
            'children': []
        }
    ]

To access the ``age`` of the **first person** (i.e. Alice) in the list, you do this:

.. code-block:: python

    data[0]['age'] # data > first item > age


*Coordinates* is  basically a string containing the chain of the keys and indices
to locate a field in the data.

.. note::
    
    To join the coordinates into a string, we use a special symbol called the **section sign** (``§``).
    Earlier, we used the hyphen (``-``) as the separator, but that made it impossible for
    the schema object keys (i.e. field names) to contain the hyphen.

So, for above example, the coordinates string is: ``'0§age'``. We've just chained the
index and key into a string.

To access the ``age`` of the **first child** (i.e. Carl) of **first person** (i.e. Alice)
in the list, you perform this lookup:

.. code-block:: python

    data[0]['children'][0]['age'] # data > first item > children > first item > age

This time, the coordinates string is: ``'0§children§0§age'``.


To make it easier to generate the coordinates string and to avoid copying and pasting
the section symbol, you can use the  :func:`~django_jsonform.utils.join_coords` helper function:

.. code-block::

    from django_jsonform.utils import join_coords

    join_coords(0, 'age') # -> '0§age'


Uses of coordinates
-------------------

1. Displaying error messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coordinates are used by the library for displaying error messages for a field.

To display error message under the age field of first person, you can do this:

.. code-block:: python

    error_map = {
        '0§age': 'Invalid value',
    }

The library will use the coordinates to display an error message under the appropriate field.

Alternatively, instead of manually copying this symbol, you can use the
:class:`~django_jsonform.utils.ErrorMap` helper class to create the error map.

2. In handler views
~~~~~~~~~~~~~~~~~~~

You can use the coordinates in a file handler view or autocomplete handler view
to determine the field in the schema which sent the request.

This is useful if you have one common handler for multiple schemas and you want to
return different response based on the schema field.

To split coordinates string into individual coordinates, use the
:func:`~django_jsonform.utils.split_coords` helper function:

.. code-block::

    from django_jsonform.utils import split_coords

    split_coords('0§age') # -> ['0', 'age']
