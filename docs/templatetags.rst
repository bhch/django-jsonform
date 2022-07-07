Template tags and filters
=========================

.. module:: django_jsonform.templatetags.django_jsonform
    :synopsis: Template tags and filters


django-jsonform provides some useful filters for working with json data in the
templates.

Usage
-----

To use the filters and tags, you'll have to first load them in a template:

.. code-block:: html

    <!-- template.html -->

    {% load django_jsonform %}



Available filters
-----------------

.. templatefilter:: parse_datetime

``parse_datetime``
~~~~~~~~~~~~~~~~~~
    
.. versionadded:: 2.9

This filter converts a date string (``'YYYY-MM-DD'``) or a datetime string in ISO format
to Python's ``datetime.datetime`` object.

django-jsonform keeps the datetime as ISO string in the database. But in templates,
you most probably would like to display the date in a nice, user-friendly format.

Use this filter to convert the string to a ``datetime`` object, and Django will
automatically format the date.

Usage:

.. code-block:: html

    {{ date_string | parse_datetime }}

    <!-- you can also use it with the date filter -->
    {{ date_string | parse_datetime | date:'d M, Y' }}

.. templatefilter:: parse_time

``parse_time``
~~~~~~~~~~~~~~
    
.. versionadded:: 2.9

This filter converts a time string (24-hour ``'HH:MM:SS'``) to Python's
``datetime.time`` object.

Usage:

.. code-block:: html

    {{ time_string | parse_time }}

    <!-- you can also use it with the time filter -->
    {{ time_string | parse_time | time:'H:i a' }}
