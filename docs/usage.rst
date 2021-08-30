Usage
=====

- Input field types
- Choices
- Uploading files
- Min and Max array items
- Adding keys
- 

Using Candy admin is similar to using Django's default admin.

Example models
--------------

Let's establish some models which will be used throughout this document for 
examples:

.. code-block:: python
    
    # models.py

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=50)
        gender = models.CharField(max_length=10)
        email = models.EmailField()

    class Post(models.Model):
        author = models.ForeignKey(Author, on_delete=models.CASCASE)
        title = models.CharField(max_length=150)
        content = models.TextField()

Registering models
------------------

Registering models is similar to Django, except you use 
:class:`django_candy.admin`:

.. code-block:: python

    # admin.py

    from django_candy import admin
    from myapp.models import Author, Post

    admin.site.register(Author)

    # Or for more control, use ModelAdmin class

    class PostAdmin(admin.ModelAdmin):
        list_display = ['title', 'author']

    admin.site.register(Post, PostAdmin)

Customising list table columns
------------------------------

You can use ``ModelAdmin.list_display`` to specify which fields appear in 
list table:

.. code-block:: python

    from django_candy import admin

    class AuthorAdmin(admin.ModelAdmin):
        list_display = ['name', 'email']

    admin.site.register(Author, AuthorAdmin)


.. _usage-list-search:

List search
-----------

Currently, Candy doesn't provide automatic search like Django's default admin 
does. Therefore, ``search_fields`` and ``get_search_results`` don't work. 

To implement search for your models, Candy provides a 
:meth:`~django_candy.admin.ModelAdmin.get_filtered_queryset` method. It receives 
a ``request``, ``queryset`` and ``query_params`` arguments. The ``query_params`` 
argument is a dict containing query parameters sent with the request. The name 
for the search query parameter is ``q`` which you can use for filtering the queryset. 

This method returns a queryset.

.. code-block:: python
    
    class AuthorAdmin(admin.ModelAdmin):
        def get_filtered_queryset(self, request, queryset, query_params):
            search_term = query_params.get('q')

            if search_term:
                queryset = queryset.filter(name__istartswith=search_term)

            return queryset


.. _usage-list-filters:

List filters
------------

Django's ``list_filter`` option doesn't work. Instead, use ``list_filters`` 
(note the extra "**s**" at the end). 

Candy doesn't provide automatic filtering either.

``list_filters`` option should be a list which contains dicts of all the 
filters and options.

Then, you can use the :meth:`~django_candy.admin.ModelAdmin.get_filtered_queryset` 
method to filter the results.

.. code-block:: python
    
    class AuthorAdmin(models.Model):
        list_filters = [
            {
                'label': 'Gender', 'name': 'gender', 'type': 'checkbox',
                'options': [
                    {'label': 'Any', 'value': '', 'default': True},
                    {'label': 'Male', 'value': 'male'},
                    {'label': 'Female', 'value': 'female'},
                ]
            },
            {
                'label': 'Sort by', 'name': 'sort_by', 'type': 'radio',
                'options': [
                    {'label': 'Name (A-Z)', 'value': 'name'},
                    {'label': 'Name (Z-A)', 'value': '-name'},
                ]
            }
        ]

        def get_filtered_queryset(self, request, queryset, query_params):
            gender = query_params.get('gender')
            sort_by = query_params.get('sort_by')

            if gender:
                queryset = queryset.filter(gender__in=gender)

            if sort_by:
                queryset = queryset.order_by(sort_by)

            return queryset