Fields and Widgets
==================

Contents:

.. contents::
    :depth: 2
    :local:
    :backlinks: none

Model fields
------------

.. module:: django_jsonform.models.fields
    :synopsis: Model fields


``JSONField``
~~~~~~~~~~~~~

.. class:: JSONField(schema=None, pre_save_hook=None, file_handler=None, **options)
    
.. versionadded:: 2.0

It is basically a subclass of Django's ``JSONField``, but for convenience,
it automatically sets up the JSON editor widget for you.


In Django < 3.1, for databases other than Postgres, it uses a ``TextField``
underneath.

**Parameters**:

.. attribute:: schema
    :type: dict, callable

    A ``dict`` or a callable object specifying the schema for the current field.

    A callable is useful for :ref:`specifying dynamic choices <dynamic choices>`.

    The callable function may optionally receive the current model instance. See:
    :ref:`Accessing model instance in callable schema`.

    .. versionchanged:: 2.1
        The ability to provide a callable was added.

    .. versionchanged:: 2.8
        Callable schema may receive an ``instance`` argument.

.. attribute:: pre_save_hook
    :type: callable

    .. versionadded:: 2.10

    (Optional) Sometimes you may wish to transform the JSON data before saving
    in the database.

    For that purpose, you can provide a callable through this argument which
    will be called before saving the field's value in the database.

    The ``pre_save_hook`` callable will receive the current value of the field
    as the only argument. It must return the value which you intend to save in
    the database.

    .. code-block::

        def pre_save_hook(value):
            # do something with the value ...
            return value


        class MyModel(...):
            items = JSONField(schema=..., pre_save_hook=pre_save_hook)

.. attribute:: file_handler
    :type: str

    .. versionadded:: 2.11

    (Optional) Provide a the url of the view for handling file uploads. See :ref:`document
    on uploading files <file url>` for usage.

.. attribute:: **options

    This ``JSONField`` accepts all the arguments accepted by Django's
    ``JSONField``, such as a custom ``encoder`` or ``decoder``.

    For details about other parameters, options and attributes of the
    ``JSONField``, see `Django's docs
    <https://docs.djangoproject.com/en/stable/ref/models/fields/#django.db.models.JSONField>`__.

Usage:

.. code-block:: python

    from django_jsonform.models.fields import JSONField


    class MyModel(models.Model):
        ITEMS_SCHEMA = {...}

        items = JSONField(schema=ITEMS_SCHEMA)


``ArrayField``
~~~~~~~~~~~~~~

.. class:: ArrayField(base_field, size=None, **options)

.. versionadded:: 2.0

A subclass of Django's ``ArrayField`` except it renders a dynamic form widget.

It takes exactly the same arguments as the original class.

It also supports multiple levels of array nesting.

Usage:

.. code-block:: python

    from django_jsonform.models.fields import ArrayField


    class MyModel(models.Model):
        items = ArrayField(models.CharField(max_length=50), size=10)
        # ...

For more details, see
`Django's docs <https://docs.djangoproject.com/en/stable/ref/contrib/postgres/fields/#arrayfield>`__.


Form fields
-----------

.. module:: django_jsonform.forms.fields
    :synopsis: Form fields

.. _form-jsonfield:

``JSONField``
~~~~~~~~~~~~~

.. class:: JSONField(schema=None, model_name='', field_name='', **options)
    
.. versionadded:: 2.0

It is a subclass of Django's ``forms.JSONField``.

**Parameters**:

.. attribute:: schema
    :type: dict, callable

    A ``dict`` or a callable object.

.. attribute:: model_name
    :type: string

    (Optional) Name of the model. It is sent along with the AJAX requests to your file handler
    view.

.. attribute:: file_handler
    :type: string

    (Optional) Provide a the url of the view for handling file uploads.

.. attribute:: **options

    It also accepts other options which are accepted by Django's ``forms.JSONField``.

    For details about other parameters, options and attributes, see `Django's docs
    <https://docs.djangoproject.com/en/4.1/ref/forms/fields/#jsonfield>`__.

Usage:

.. code-block:: python

    from django_jsonform.forms.fields import JSONField

    class MyForm(forms.Form):
        my_field = JSONField(schema=schema)

Widgets
-------

.. module:: django_jsonform.widgets
    :synopsis: Widgets


``JSONFormWidget``
~~~~~~~~~~~~~~~~~~

.. class:: JSONFormWidget(schema, model_name='', file_handler='', validate_on_submit=False, attrs=None)
    
The widget which renders the editor.

It can be used in a form if you don't want to use the model field.

**Parameters**:

.. attribute:: schema
    :type: dict, callable

    A ``dict`` or a callable object specifying the schema for the current field.

    A callable is useful for :ref:`specifying dynamic choices <dynamic choices>`.

    The callable function may optionally receive the current model instance.
    See: :ref:`Accessing model instance in callable schema`.

    .. versionchanged:: 2.1
        The ability to provide a callable was added.

    .. versionchanged:: 2.8
        Callable schema may receive an ``instance`` argument.

.. attribute:: model_name
    :type: str

    (Optional). The name of the model. It is passed to the file upload handler
    so that you can identify which model is requesting the file upload.

    See :ref:`Handling file uploads` for more details.

.. attribute:: file_handler
    :type: str

    .. versionadded:: 2.11

    (Optional) Provide a the url of the view for handling file uploads. See :ref:`document
    on uploading files <file url>` for usage.

.. attribute:: validate_on_submit
    :type: bool

    .. versionadded:: 2.12

    (Optional) Whether to validate the data on the browser when form is submitted.

    Default ``False``.
    
    See :ref:`Validating data in browser <validate-on-submit>` for more.

.. attribute:: attrs
    :type: dict

    .. versionadded:: 2.12

    (Optional) A dictionary mapping of HTML attributes and values for the widget
    container element.

Usage:

.. code-block:: python

    # admin.py

    from django_jsonform.widgets import JSONFormWidget
    from myapp.models import ShoppingList


    class ShoppingListForm(forms.ModelForm):
        class Meta:
            model = ShoppingList
            fields = '__all__'
            widgets = {
                'items': JSONFormWidget(schema=ShoppingList.ITEMS_SCHEMA)
            }

    class ShoppingListAdmin(admin.ModelAdmin):
        form = ShoppingListForm

    admin.site.register(ShoppingList, ShoppingListAdmin)


This widget can not be used directly with Django's ``ArrayField`` because
Django's ``ArrayField`` converts the value from array to a string before passing
it to the widget whereas it expects a list or a dict.


Accessing model instance in callable schema
-------------------------------------------

.. versionadded:: 2.8

Automatically accessing model instance in a widget is not possible. This is due
the way Django initialises the widgets and form fields.

However, you can bypass this limitation by manually setting an ``instance``
attribute on the widget.

To do this, you are required to create a custom form class for your model:

.. code-block::

    # models.py

    def callable_schema(instance=None):
        # instance will be None while creating new object
        
        if instance:
            # ... do something with the instance ...
        else:
            # ... do something else ...        
        return schema


    class MyModel(models.Model):
        my_field = JSONField(schema=callable_schema)


    ...

    # admin.py

    # create a custom modelform
    class MyModelForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # manually set the current instance on the widget
            self.fields['my_field'].widget.instance = self.instance


    # set the form on the admin class
    class MyAdmin(admin.ModelAdmin):
        form = MyModelForm


    admin.site.register(MyModel, MyAdmin)


Your callable schema function will get the current model ``instance`` on *Edit/Change*
admin page. It will be ``None`` on the *Add new* page (*i.e.* while creating new objects).
