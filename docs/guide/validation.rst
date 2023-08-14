Validation
==========

.. versionadded:: 2.12

django-jsonform supports basic data validation by default and appropriate error
messages are displayed below the input fields in case any value is invalid.

Validation keywords
-------------------

For ``array`` type
~~~~~~~~~~~~~~~~~~

=============== ===========
Keyword         Description
=============== ===========
``minItems``    (*Integer*) Minimum number or required items.
``maxItems``    (*Integer*) Maximum number of allowed items.
``uniqueItems`` (*Boolean*) Whether all items must be unique or not.
=============== ===========

For ``object`` type
~~~~~~~~~~~~~~~~~~~

=============== ===========
Keyword         Description
=============== ===========
``required``    (*List*) A list containing names of required object properties (keys).
=============== ===========

.. versionchanged:: 2.16.0
    Support for ``required`` keyword for object properties was added.


For ``string`` type
~~~~~~~~~~~~~~~~~~~

============= ===========
Keyword       Description
============= ===========
``required``  (*Boolean*) Whether this field is required or not.
``minLength`` (*Integer*) Minimum length of the value.
``maxLength`` (*Integer*) Maximum allowed length of the value.
============= ===========

For ``integer`` and ``number`` type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

==================== ===========
Keyword              Description
==================== ===========
``required``         (*Boolean*) Whether this field is required or not.
``minimum``          (*Integer/Float*) Minimum allowed value including this limit.
``maximum``          (*Integer/Float*) Maximum allowed value including this limit.
``exclusiveMinimum`` (*Integer/Float*) Minimum allowed value excluding this limit.
``exclusiveMaximum`` (*Integer/Float*) Maximum allowed value excluding this limit.
==================== ===========

For ``boolean`` type
~~~~~~~~~~~~~~~~~~~~

============= ===========
Keyword       Description
============= ===========
``required``  (*Boolean*) Whether this field is required or not.
============= ===========

Example
~~~~~~~

.. code-block:: python
    :emphasize-lines: 5, 11, 12, 16

    # Schema

    {
        'type': 'array',
        'minItems': 1,
        'items': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'required': True,
                    'maxLength': 30
                },
                'age': {
                    'type': 'integer',
                    'minimum': '18'
                }
            }
        }
    }


Custom validation
-----------------

There are many ways to validate a field in Django.

Two of the most basic ways are either by using the ``Model.clean()`` method or by
passing a ``validators`` argument to the model field.

The problem with these validation methods is that there is no way to provide
error messages for particular input fields.

The error message you return will be displayed above the JSON form widget.


Basic validation
~~~~~~~~~~~~~~~~

- ``Model.clean()``: Refer to Django docs on using `Model.clean() <https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.clean>`__ method.
- ``validators``: Refer Django docs on using `Validators <https://docs.djangoproject.com/en/4.1/ref/validators/>`__.


Advanced validation
~~~~~~~~~~~~~~~~~~~

Advanced validation allows you to provide error messages for each input field
which will be displayed right below them.

Creating a form
^^^^^^^^^^^^^^^

For this, you're required to create a custom form class for the admin page.

.. code-block:: python
    :emphasize-lines: 14,15

    # models.py

    class ShoppingList(models.Model):
        items = JSONField(schema=...)

    ...

    # admin.py

    class ShoppingListForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # set your validators on the form field
            self.fields['items'].validators = [items_validator]


    class ShoppingListAdmin(admin.ModelAdmin):
        form = ShoppingListForm


Writing the validator
^^^^^^^^^^^^^^^^^^^^^

In your validator function, instead of raising ``ValidationError``
you must raise :class:`~django_jsonform.exceptions.JSONSchemaValidationError`. This exception allows you to pass
error messages for individual input field in the widget.

We'll use the :class:`~django_jsonform.utils.ErrorMap` helper class to create
the mapping of field names to error messages:

.. code-block:: python

    from django_jsonform.exceptions import JSONSchemaValidationError
    from django_jsonform.utils import ErrorMap

    def items_validator(value):
        error_map = ErrorMap()

        if value[0] != 'Banana':
            error_map.set(coords=[0], msg='First item in shopping list must be Banana')

        if value[1] != 'Eggs':
            error_map.set(coords=[1], msg='Second item in shopping list must be Eggs')

        # do other validations ...

        if error_map:
            # if error_map has keys raise error
            raise JSONSchemaValidationError(
                'Please correct errors below',
                error_map=error_map # pass error_map to exception
            )


For passing multiple error messages for one input, use a list:

.. code-block:: python

    # using ErrorMap.set()
    error_map.set(coords=[0], msg=['First error', 'Second error', ...])

    # or useing ErrorMap.append()
    error_map.append(coords=[0], msg=['First error', 'Second error', ...])


See :class:`~django_jsonform.utils.ErrorMap` class's docs for more details on its
usage.


Providing errors for deeply nested inputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The keys in the ``error_map`` dict are *"coordinates"* of the invalid input fields
(see :doc:`/guide/coordinates` page to learn more).

For example, if each shopping list item has a ``name`` and a ``quantity`` and you want
to display an error message under the first item's ``quantity`` input, you'll do this:

.. code-block:: python

    from django_jsonform.utils import ErrorMap

    error_map = ErrorMap()

    # error message for 'quantity' of '0' (first item)
    error_map.set(coords=[0, 'quantity'], msg='Minimum quantity must be 5')


.. _validate-on-submit:

Validating data in the browser before form submission
-----------------------------------------------------

The JavaScript part of this widget supports optional in-browser validation.

The data will be validated before the form is submitted. If there are any errors,
the form will not submit and user will be asked to correct them.

This method only supports basic validation. When the data has passed the browser
validation tests, it will be validated once again on the server with your custom
validation rules.

To enable in-browser validation, set the ``validate_on_submit`` attribute to 
``True`` on the widget.

There are two ways to do this:

**Option 1**: Changing the attribute on the widget:

.. code-block:: python
    :emphasize-lines: 7

    # Option 1: In form's __init__ method

    class ShoppingListForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['items'].widget.validate_on_submit = True


**Option 2**: Alternatively, if you're overriding the widget in the ``Meta`` class,
you can pass the ``validate_on_submit`` argument to the widget:

.. code-block:: python
    :emphasize-lines: 6

    # Option 2: In form's Meta class

    class ShoppingListForm(forms.ModelForm):
        class Meta:
            widgets: {
                'items': JSONFormWidget(schema=..., validate_on_submit=True)
            }


Built-in validators
-------------------

.. module:: django_jsonform.validators
    :synopsis: Built-in validators

``JSONSchemaValidator``
~~~~~~~~~~~~~~~~~~~~~~~

.. class:: JSONSchemaValidator(schema)

.. versionadded:: 2.12

This is the default validator used for validating the submitted forms.

**Parameters**:

.. attribute:: schema
    :type: dict

    Schema to use for validation.

**Methods**:

.. method:: validate(data)

    Validates the ``data`` against the schema provided to the validator instance.

    If the data is invalid, it will raise :class:`~django_jsonform.exceptions.JSONSchemaValidationError`
    exception.

**Usage**:

.. code-block:: python

    from django_jsonform.validators import JSONSchemaValidator

    # create a validator instance
    validator = JSONSchemaValidator(schema=...)

    # validate the data
    validate(data)

    # if the data is invalid, JSONSchemaValidationError will be raised


Exceptions
----------

.. module:: django_jsonform.exceptions
    :synopsis: Exceptions

``JSONSchemaValidationError``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: JSONSchemaValidationError(message, code=None, params=None, error_map=None)
    
.. versionadded:: 2.12

It is a subclass of Django's ``ValidationError``. It accepts one extra argument
called ``error_map``.

**Parameters**:

.. attribute:: error_map
    :type: ErrorMap

    An instance of :class:`~django_jsonform.utils.ErrorMap` class for providing
    the errors for widget's input fields.
