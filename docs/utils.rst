Utilities
=========

.. module:: django_jsonform.utils
    :synopsis: Helper functions and classes

Helper functions and classes.


``ErrorMap``
------------

.. class:: ErrorMap()

.. versionadded:: 2.15

It is basically a subclass of ``dict`` but it makes it easier to create an error
mapping for the widget.

**Methods**

.. method:: set(coords, msg)

    Set the given message for the given coordinates.

    ``coords`` - A ``list`` of coordinates of the field.

    ``msg`` - A ``string`` or a ``list`` of error messages.

.. method:: append(coords, msg)

    Append the given message to previously added coordinates. If the coordinates
    don't exit, it acts like the ``set()`` method.


    ``coords`` - A ``list`` of coordinates of the field.

    ``msg`` - A ``string`` or a ``list`` of error messages.

Usage:

.. code-block::

    from django_jsonform.utils import ErrorMap

    error_map = ErrorMap()

    # set an error message
    error_map.set(coords=[0], msg='This value is invalid')

    # append error messages on same field
    error_map.append(coords=[0], msg='Second error message')

    print(error_map)

    {'0': ['This value is invalid', 'Second error message']}


``join_coords``
---------------

.. function:: join_coords(*coords)

.. versionadded:: 2.15

Generates a string by joining the given coordinates.

Internally, we use the section sign (``§``) for joining the coordinates. Earlier,
a hyphen (``-``) was used, but that caused some complications when a key in a 
scheka (i.e. a field name) had a hyphen in it as it was impossible to know whether the
hyphen was the separator or part of the key.

Now, this symbol is chosen because it's very rarely used.

.. code-block::

    from django_jsonform.utils import join_coords

    join_coords('person', 0, 'name') # -> 'person§0§name'


``split_coords``
----------------

.. function:: split_coords(coords)

.. versionadded:: 2.15

Splits a coordinates string into individual coordinates.

The section sign (``§``) is used for splitting the coordinates.

.. code-block::

    from django_jsonform.utils import split_coords

    split_coords('person§0§name') # -> ['person', '0', 'name']
