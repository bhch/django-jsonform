Schema Guide
============


Types
-----

``array``:
    Equivalent of a list in Python.
    Requires an ``items`` key.
``object``:
    Equivalent of a dict in Python.
    Requires a ``keys`` key.
``string``:
    A string input.
``number``:
    A number.
``float``:
    A floating point number.

Candy provides its own :class:`~django_candy.admin.ModelAdmin` and :class:`AdminSite` 
classes. You can't use Django's ``ModelAdmin`` with Candy.

Import ``admin`` from ``django_candy``:

.. code-block:: python

    from django_candy import admin


``array``
---------

``search_fields`` and ``get_search_results`` don't work in Candy.

Use :meth:`~django_candy.admin.ModelAdmin.get_filtered_queryset` to implement 
searching and filtering. 

See :ref:`Usage docs on list search <usage-list-search>` for details.


List filters
------------

Django admin's ``list_filter`` doesn't work. Instead, use ``list_filters`` 
(note the extra "**s**" at the end).

And Candy doesn't provide automatic filtering. You're required to filter the 
results yourself using :meth:`~django_candy.admin.ModelAdmin`. 

See :ref:`Usage docs on list filters <usage-list-filters>` for details.

