Input field types
=================

There are four values for the ``type`` keyword which have an input field:

1. ``string`` - For text, email, date, file, and other inputs.
2. ``number`` - For number input (including floats).
3. ``integer`` - For integer only number input.
4. ``boolean`` - For ``True`` - ``False`` inputs (checkbox by default).

We've excluded ``array`` and ``object`` types as they can't have input fields.


.. _inputs for string type:

Inputs for ``string`` type
--------------------------

The input fields for ``string`` values can be customized using the ``format``
and ``widget`` keywords.

Available ``format`` values for ``string`` type:

============= ===========
Format        Description
============= ===========
``color``     A colour input
``date``      A date input
``date-time`` A datetime input. See :ref:`Datetime field` for details.
``datetime``  Alias for ``date-time``
``email``     An email input
``password``  A password input
``time``      A time input
``data-url``  A file input. See :doc:`Uploading files <upload>` for usage.
``file-url``  A file input. See :doc:`Uploading files <upload>` for usage.
============= ===========

Available ``widget`` values for ``string`` type:

================ ===========
Widget           Description
================ ===========
``textarea``     A textarea input
``radio``        A radio input (:doc:`useful for choices </guide/choices>`)
``multiselect``  A multiselect drowpdown input (:doc:`useful for choices </guide/choices>`)
``autocomplete`` Useful for fetching options via AJAX requests (:doc:`See usage </guide/autocomplete>`)
``fileinput``    A file input. Useful for overriding ``file-url`` input (:ref:`See usage <Overriding the file input>`)
``hidden``       A hidden input
================ ===========


Examples:

.. code-block:: python

    # 1. Text input (default)
    {
        'type': 'string'
    }

    
    # 2. Date input
    {
        'type': 'string',
        'format': 'date'
    }


    # 3. Email input
    {
        'type': 'string',
        'format': 'email'
    }

    # 4. Textarea input
    {
        'type': 'string',
        'widget': 'textarea'
    }

    # ...


Inputs for ``number`` and ``integer`` types
-------------------------------------------

The ``number`` and ``integer`` types get an HTML ``number`` input field by default.
These can be customized using the ``widget`` keyword.

Available ``widget`` values for ``number`` & ``integer`` type:

================ ===========
Widget           Description
================ ===========
``range``        A range HTML input.
================ ===========


Inputs for ``boolean`` type
---------------------------

The ``boolean`` type gets an HTML ``checkbox`` input. Currently, it can't be 
customized to another input type.

However, you can use :doc:`choices <choices>` to display a ``radio`` or ``select``
input with *Yes/No* options to choose from.


Default values
--------------

.. versionadded:: 2.6

You can specify default initial values for inputs using the ``default`` keyword:

.. code-block:: python

    # 1. String input
    {
        'type': 'string',
        'default': 'Hello world'
    }

    # 2. Boolean
    {
        'type': 'boolean',
        'default': True
    }

    # 3. Default choice
    {
        'type': 'string',
        'choices': ['Eggs', 'Juice', 'Milk'],
        'default': 'Milk'
    }

    # 4. Default array items
    {
        'type': 'array',
        'items': {
            'type': 'string',
            'default': 'Hello world' # default value for every new array item
        }
    }


Readonly inputs
---------------

.. versionadded:: 2.6

You can make inputs uneditable using a ``readonly`` (alias ``readOnly``) keyword:

.. code-block:: python

    # 1. String inputs
    {
        'type': 'string',
        'readonly': True
    }

    # 2. Array items
    {
        'type': 'array',
        'items': {
            'type': 'string',
            'readonly': True # all items will be readonly
        }
    }

.. seealso::

    To make the whole form readonly instead of individual fields, see:
    :ref:`Making the whole JSON form readonly`.

Datetime field
--------------

.. versionadded:: 2.8

Usage:

.. code-block:: python

    {
        'type': 'string',
        'format': 'datetime' # or 'date-time'
    }

The value will be saved as ISO formatted date, such as: ``2022-02-06T15:42:11.000+00:00``.

Timezone conversion
~~~~~~~~~~~~~~~~~~~

When a user selects the time on their browser, it will be interpreted in their
operating system's local timezone. Then, the widget will convert it to UTC for
saving in the database.

Also, the widget's time picker is in 12-hour format, but the final value will be
converted to 24-hour format.

Example: Suppose there's a user whose timezone is +5:30 (Indian Standard Time). If that user inputs
``10:00:00 pm``, the widget will convert it to UTC time and 24-hour format.
The final value you'll get is ``16:30:00``.

This timezone conversion only happens on the ``datetime`` field. It doesn't affect ``date`` field 
or ``time`` field.

Formatting datetime
~~~~~~~~~~~~~~~~~~~

The widget keeps the datetime value as an ISO string for JSON compatibility.

However, you may want to format a date value such as to display in the templates
in a user-friendly format.

Formatting datetime in templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

django-jsonform provides a few template filters to convert the date string to a
``datetime`` object so you can use it with Django's ``date`` filter.

You can use the :tfilter:`parse_datetime` filter (*New in version 2.9*) for this:

.. code-block:: html

    <!-- template.html -->
    {% load django_jsonform %}

    {{ date_string | parse_datetime }}

    <!-- you can also use it with the date filter -->
    {{ date_string | parse_datetime | date:'d M, Y' }}



All the available tags and filters are listed in :doc:`Template tags and filters </templatetags>`
document.

Formatting datetime in Python code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To format datetime string in Python code, you'll have to first convert the string
to Python's ``datetime`` object:

.. code-block:: python

    from datetime import datetime

    date_string = '2022-02-06T15:42:11.092+00:00' # ISO string

    date = datetime.fromisoformat(date_string)

    # ... do something with the object ...
