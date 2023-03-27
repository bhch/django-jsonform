Schema guide
============

django-jsonform currently implements a custom JSON Schema spec written
specifically for Django.

You should also read the standard spec at
`https://json-schema.org <https://json-schema.org/learn/getting-started-step-by-step>`_.

At present, certain features from the standard spec are not supported by
django-jsonform. However, we've also implemented a few extra features which are
not in the standard spec.

For some complex schema examples, see :doc:`Examples page <examples>`.

For data validation, see :doc:`Validation page </guide/validation>`.


Types
-----

Currently, only these six types are supported:

.. contents::
    :depth: 1
    :local:
    :backlinks: none


``array`` (alias ``list``)
~~~~~~~~~~~~~~~~~~~~~~~~~~

A JSON array (similar to Python list).

Keywords:

================================== ===========
Keyword                            Description
================================== ===========
``items`` (**required**)           Specifies the scheme for the items allowed in the list.
``title``                          Specify a title for the list.
``default``                        A list containing all the default initial values for the array.
================================== ===========

:doc:`Validation </guide/validation>` keywords:

================================== ===========
Keyword                            Description
================================== ===========
``minItems`` (alias ``min_items``) Limit the minimum number of items in a list.
``maxItems`` (alias ``max_items``) Limit the maximum number of items in a list.
``uniqueItems``                    Whether all items in the list must be unique or not.
================================== ===========

.. versionchanged:: 2.8
    Support for setting initial array data using ``default`` keyword was added.

.. versionchanged:: 2.12
    Support for ``uniqueItems`` keyword was added.

This example shows a schema of a list containing string items:

.. code-block:: python

    # Schema
    {
        'type': 'list', # or 'array'
        'items': {
            'type': 'string',
            'default': 'Hello', # default value for new items
            'readonly': True, # make all items readonly
        },
        'minItems': 1,
        'maxItems': 5,
        'default': ['One', 'Two', 'Three'], # initial value for the whole list
    }


    # Output data
    ['one', 'two', 'three', ...]


``object`` (alias ``dict``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A JSON object (similar to Python dict).

Keywords:

================================== ===========
Keyword                            Description
================================== ===========
``properties`` (alias ``keys``)    Specifies the keys (or fields) in a dict/object.
``additionalProperties``           Allow users to add extra keys not declared in the schema.
``title``                          Specify a title for the dict.
``required``                       A list containing names of required object properties (keys).
================================== ===========

.. versionchanged:: 2.16.0
    Support for ``required`` keyword for object properties was added.

This example shows a schema of a basic dict:

.. code-block:: python

    # Schema
    {
        'type': 'dict': # or 'object'
        'keys': { # or 'properties'
            'name': {
                'type': 'string'
            },
            'email': {
                'type': 'string'
            },
            'age': {
                'type': 'number',
                'title': 'Age in years',
                'default': 50, # default value for age
                'readonly': True, # make it readonly
            }
        },
        'required': ['email']
    }


    # Output data
    {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 99
    }


Additional keys
^^^^^^^^^^^^^^^

By default, an object's data can only contain keys declared in the schema.
But you can allow users to add extra keys using the ``additionalProperties``
keyword.

The ``additionalProperties`` keyword can be:

- **a schema**. You can provide a sub-schema for the new properties.
- **a boolean**. As a shortcut for adding string keys only, you can set this to
  ``True``.
- **a reference**. You can also use the ``$ref`` keyword to reference and reuse
  existing schema. See :ref:`referencing schema` docs below to learn more.

.. versionchanged:: 2.10 Support for sub-schema for new properties was added.

.. code-block:: python
    :emphasize-lines: 8, 10, 12

    # Schema
    {
        'type': 'dict', # or 'object'
        'keys': { # or 'properties'
            'name': { 'type': 'string' },
        },
        
        'addtionalProperties': True

        # or
        
        'additionalProperties': { 'type': 'string' }
    }

    # Output data
    {
        'name': 'John Doe', # declared in the schema
        'gender': 'Male', # added by the user
    }


``string``
~~~~~~~~~~

A string.

This can't be at the top level of the schema. If you only want to save
a string, you should use Django's ``CharField``.

Keywords:

================================== ===========
Keyword                            Description
================================== ===========
``title``                          Specify the label for the input field.
``choices`` (alias ``enum``)       | Specify choices for the field.
                                   | See the :doc:`document on Choices <guide/choices>` for more.
``format``                         | Use this to specify the input field type.
                                   | See :ref:`inputs for string type` for more.
``widget``                         | Use this to specify the input field type, such as a textarea.
                                   | For most use cases, prefer the ``format`` keyword.
``default``                        Specify a default value for this input field.
``readonly`` (alias ``readOnly``)  Make this input field readonly.
``helpText`` (alias ``help_text``) Display a help text under this input.
``placeholder``                    Placeholder text for this input.
================================== ===========

:doc:`Validation </guide/validation>` keywords:

==================== ===========
Keyword              Description
==================== ===========
``required``         Whether this field is required or not.
``minLength``        Minimum required length.
``maxLength``        Maximum allowed length.
==================== ===========

.. versionchanged:: 2.6
    Support for ``default`` and ``readonly`` keywords was added.

.. versionchanged:: 2.9
    Support for ``helpText`` (or ``help_text``) keywords was added.

.. versionchanged:: 2.11
    Support for ``placeholder``, ``enum`` and ``handler`` keywords was added.

.. versionchanged:: 2.12
    Support for ``required``, ``minLength`` and ``maxLength`` keywords was added.

``number``
~~~~~~~~~~

A number (including floats).

This can't be at the top level of the schema. If you only want to save a number,
you should use Django's ``FloatField``.

It gets a ``number`` HTML input by default. It can be overridden using the ``range``
widget.

Keywords:

================================== ===========
Keyword                            Description
================================== ===========
``title``                          Specify the label for the input field.
``choices`` (alias ``enum``)       | Specify choices for the field.
                                   | See the :doc:`document on Choices <guide/choices>` for more.
``widget``                         Use this to specify the input field type, such as a range input.
``default``                        Specify a default numerical value for this input field.
``readonly`` (alias ``readOnly``)  Make this input field readonly.
``helpText`` (alias ``help_text``) Display a help text under this input.
``placeholder``                    Placeholder text for this input.
================================== ===========

:doc:`Validation </guide/validation>` keywords:

==================== ===========
Keyword              Description
==================== ===========
``required``         Whether this field is required or not.
``minimum``          Minimum allowed value including this limit.
``maximum``          Maximum allowed value including this limit.
``exclusiveMinimum`` Minimum allowed value excluding this limit.
``exclusiveMaximum`` Maximum allowed value excluding this limit.
==================== ===========

.. versionchanged:: 2.6
    Support for ``default`` and ``readonly`` keywords was added.

.. versionchanged:: 2.9
    Support for ``helpText`` (or ``help_text``) keywords was added.

.. versionchanged:: 2.11
    Support for ``placeholder`` and ``enum`` keywords was added.

.. versionchanged:: 2.12
    Support for ``required``, ``minimum`` and ``maximum``, ``exclusiveMinimum``
    and ``exclusiveMaximum`` keywords was added.

``integer``
~~~~~~~~~~~

An integer.

This can't be at the top level of the schema. If you only want to save an
integer, you should use Django's ``IntegerField``.

It gets a ``number`` HTML input by default. It can be overridden using the ``range``
widget.

Keywords:

================================== ===========
Keyword                            Description
================================== ===========
``title``                          Specify the label for the input field.
``choices`` (alias ``enum``)       | Specify choices for the field.
                                   | See the :doc:`document on Choices <guide/choices>` for more.
``widget``                         Use this to specify the input field type, such as a range input.
``default``                        Specify a default numerical value for this input field.
``readonly`` (alias ``readOnly``)  Make this input field readonly.
``helpText`` (alias ``help_text``) Display a help text under this input.
``placeholder``                    Placeholder text for this input
================================== ===========

:doc:`Validation </guide/validation>` keywords:

==================== ===========
Keyword              Description
==================== ===========
``required``         Whether this field is required or not.
``minimum``          Minimum allowed value including this limit.
``maximum``          Maximum allowed value including this limit.
``exclusiveMinimum`` Minimum allowed value excluding this limit.
``exclusiveMaximum`` Maximum allowed value excluding this limit.
==================== ===========

.. versionchanged:: 2.6
    Support for ``default`` and ``readonly`` keywords was added.

.. versionchanged:: 2.9
    Support for ``helpText`` (or ``help_text``) keywords was added.

.. versionchanged:: 2.11
    Support for ``placeholder`` and ``enum`` keywords was added.

.. versionchanged:: 2.12
    Support for ``required``, ``minimum`` and ``maximum``, ``exclusiveMinimum``
    and ``exclusiveMaximum`` keywords was added.

``boolean``
~~~~~~~~~~~

A boolean.

This can't be at the top level of the schema. If you only want to save an boolean,
you should use Django's ``BooleanField``.

It gets a ``checkbox`` HTML input by default. It can't be overridden.

Keywords:

================================== ===========
Keyword                            Description
================================== ===========
``title``                          Specify the label for the input field.
``choices`` (alias ``enum``)       | Specify choices for the field.
                                   | See the :doc:`document on Choices <guide/choices>` for more.
``widget``                         Use this to specify the input field type, such as a radio input.
``default``                        Specify a default boolean value for this input field.
``readonly`` (alias ``readOnly``)  Make this input field readonly.
``helpText`` (alias ``help_text``) Display a help text under this input.
================================== ===========

:doc:`Validation </guide/validation>` keywords:

==================== ===========
Keyword              Description
==================== ===========
``required``         Whether this field is required or not.
==================== ===========

.. versionchanged:: 2.6
    Support for ``default`` and ``readonly`` keywords was added.

.. versionchanged:: 2.9
    Support for ``helpText`` (or ``help_text``) keywords was added.

.. versionchanged:: 2.12
    Support for ``required`` keyword was added.


Referencing schema
------------------

.. versionadded:: 2.10

JSON schema specification allows you to reference parts of schema for reuse in
multiple places. This feature also allows you to recursively nest an object
within itself.


``$ref`` keyword
~~~~~~~~~~~~~~~~

Use the ``$ref`` keyword to reference other parts of the schema.

In the following example, ``shipping_address`` has same fields as
``billing_address``. So, instead of defining the schema twice, you can reference
the earlier defined schema.

.. code-block:: python
    :emphasize-lines: 12

    {
        'type': 'object',
        'properties': {
            'billing_address': {
                'type': 'object',
                'properties': {
                    'street': { 'type': 'string' },
                    'city': { 'type': 'string' },
                    'state': { 'type': 'string' }
                }
            },
            'shipping_address': { '$ref': '#/properties/billing_address' }
        }
    }


``$defs`` keyword
~~~~~~~~~~~~~~~~~

You can define common schema and keep them in a single place under the ``$defs``
object:

.. code-block:: python
    :emphasize-lines: 5, 8, 12

    {
        'type': 'object',
        'properties': {
            'billing_address': {
                '$ref': '#/$defs/address'
            },
            'shipping_address': {
                '$ref': '#/$defs/address'
            }
        },

        '$defs': {
            'address': {
                'type': 'object',
                'properties': {
                    'street': { 'type': 'string' },
                    'city': { 'type': 'string' },
                    'state': { 'type': 'string' }
                }
            }
        }
    }


.. seealso::

   `Structuring a complex schema <https://json-schema.org/understanding-json-schema/structuring.html>`__
      Official documentation on referencing and nesting on JSON Schema's website


Recursive nesting
-----------------

The ``$ref`` keyword also makes recursion possible. You can use it for
recursively nesting an object within itself.

For example, a Menu object can have link items and a sub-menu (dropdown menu)
which contains more links and a sub-sub-menu and so on...

.. code-block:: python
    :emphasize-lines: 15

    {
        'type': 'array',
        'title': 'Menu',
        'items': {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                    'title': 'Display text for the item'
                },
                'link': {
                    'type': 'string',
                    'title': 'URL of the item'
                },
                'children': { '$ref': '#' }
            }
        }        
    }

.. caution::

    **Beware of the infinite loop** while referencing.

    In certain cases, referencing (``$ref``) may cause an infinite loop.
    Currently, that error is unhandled, and the widget will not be rendered at
    all if that happens.

    One particular case is when two objects reference each other. For example,
    ``a`` is a reference to ``b`` and ``b`` is a reference to ``a``.

    There might be other cases, too. If the widget doesn't render while you're
    using ``$ref``, please open your browser's dev console to check the error
    message.

    Also, `open an issue on Github <https://github.com/bhch/django-jsonform/issues>`__.

    Infinite loop error handling will be improved in a future release.


.. _oneof-anyof-allof:

``oneOf``, ``anyOf`` and ``allOf``
----------------------------------

.. versionadded:: 2.16.0

The widget provides support for ``oneOf``, ``anyOf`` and ``allOf``, however, with
certain limitations.

``oneOf``
~~~~~~~~~

.. versionadded:: 2.16.0


**Limitations:**

1. As per the JSON schema specification, ``oneOf`` means exactly one subschema
   should match the data. If multiple matches are found, then that should be treated
   as invalid. But the built-in validation doesn't make that check. It only checks
   for *at least one* match (not *exactly one* match). If this is something you
   care about, you are advised to write :ref:`custom validation <custom validation>`.
2. Can't be used with ``additionalProperties``.

.. code-block:: python

    {
        'type': 'object',
        'oneOf': [
            {
                'properties': {
                    'age': {'type': 'number'} 
                }
            },
            {
                'properties': {
                    'date_of_birth': {'type': 'string', 'format': 'date-time'} 
                }
            }
        ]
    }


``anyOf``
~~~~~~~~~

.. versionadded:: 2.16.0


**Limitations:**

1. Can't be used with ``additionalProperties``.

.. code-block:: python

    {
        'type': 'array',
        'items': {
            'anyOf': [
                {'type': 'number'},
                {'type': 'string'}
            ]
        }
    }


``allOf``
~~~~~~~~~

.. versionadded:: 2.16.0


**Limitations:**

1. Can only be used inside ``object`` type. Will not work inside arrays or other
   types as it may lead to conflicting subschemas.

.. code-block:: python

    {
        'type': 'object',
        'allOf': {
            'properties': {
                'age': {'type': 'number'} 
            },
            'properties': {
                'date_of_birth': {'type': 'string', 'format': 'date-time'} 
            },
        },
        'additionalProperties': True # additionalProperties can be used with allOf
    }