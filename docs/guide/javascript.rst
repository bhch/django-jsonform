JavaScript API
==============

.. versionadded:: 2.11

This document describes the JavaScript API available for django-jsonform widget.

**Some use cases**:

- Dynamically modifying schema directly in the browser
- Enabling/disabling inputs dynamically
- Updating choices dynamically
- Making AJAX requests on value changes


API
---

.. note::

    django-jsonform uses `react-json-form <https://github.com/bhch/react-json-form/>`_
    under the hood.

    So, this is a shortened documentation of the actual API. We'll only look at
    the functions which concern the widget.


``reactJsonForm.getFormInstance(id)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this function to get an instance of the form widget.

The ``id`` is the ID of the widget container which looks like this: ``id_<field-name>_jsonform``.

E.g., if your model's JSONField is called "my_field", then the container id will be
``id_my_field_jsonform``.

You can also do *Right-click > Inspect element* on the form widget to view the ID of 
the container.

.. code-block:: javascript

    var form = reactJsonForm.getFormInstance('id_my_field_jsonform');


``formInstance.addEventListener(event, callback)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this function to add a ``callback`` function for an ``event``. It will be called
every time the event occurs.

The callback will receive an object containing these keys:

- ``data``: The data of the widget
- ``schema``: The schema of the widget
- ``prevData``: Previous data (before the event)
- ``prevSchema``: Previous schema (before the event)

.. code-block:: javascript

    function onChangeHandler(e) {
        // do something ...
    }

    var form = reactJsonForm.getFormInstance('id_my_field_jsonform');

    form.addEventListener('change', onChangeHandler);


``formInstance.update(config)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this function to update the schema or the data of the widget.


The ``config`` is a JavaScript object (dict) which looks like this:

.. code-block:: javascript

    var config = {
        schema: ...,
        data: ...,
    }

    form.update(config);


.. important::
    If you call the ``update`` function from a ``change`` event listener, it is important
    that you call it conditionally. Otherwise, it might lead to an infinite loop.

    For example, call this function if the current data (``data``) and the previous data
    (``prevData``) are not the same. This way you can avoid the infinite loop.


``formInstance.getData()``      
~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the current data of the form instance.

``formInstance.getSchema()``      
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the current schema of the form instance.


Practical example
-----------------

**Updating choices dynamically**: Let's look at an example where there are two select inputs and choices of the
second input depends on the first input.


Interactive Demo
~~~~~~~~~~~~~~~~

In the following demo, **Vehicle** input's ``choices`` and ``helpText`` will change
dynamically depending upon the value of the **Category** input.

.. raw:: html


    <iframe height="450" style="width: 100%; margin-bottom: 45px;" scrolling="no" title="django-jsonform JS API demo" src="https://codepen.io/bhch/embed/zYdbJEq?default-tab=result" frameborder="no" loading="lazy" allowtransparency="true" allowfullscreen="true">
      See the Pen <a href="https://codepen.io/bhch/pen/zYdbJEq">
      django-jsonform JS API demo</a> by Bharat Chauhan (<a href="https://codepen.io/bhch">@bhch</a>)
      on <a href="https://codepen.io">CodePen</a>.
    </iframe>


Schema
~~~~~~

The schema for this demo:

.. code-block:: python

    {
        'type': 'object',
        'title': 'Mode of transportation',
        'keys': {
            'category': {
                'type': 'string',
                'choices': ['Land', 'Water', 'Air']
            },
            'vehicle': {
                'type': 'string',
                'choices': [] # vehicle choices will be added dynamically
            }
        }
    }


JavaScript code
~~~~~~~~~~~~~~~

Following is the code which is used in the demo above:

.. code-block:: javascript

    // my-script.js

    window.addEventListener('load', function() {
        /* We want to run this code after all other scripts have been loaded */

        if (window.reactJsonForm) {
            /* We put this inside a condition because 
             * we only want it to run on those pages where
             * django-jsonform widget is loaded
             */
            var form = reactJsonForm.getFormInstance('id_my_field_jsonform');
            form.addEventListener('change', onJsonFormChange);
        }
    });


    var vehicleChoiceMap = {
        'Land': ['Car', 'Bus', 'Train'],
        'Water': ['Ship', 'Boat', 'Submarine'],
        'Air': ['Aeroplane', 'Rocket'],
    };


    function onJsonFormChange(e) {
        var data = e.data; // current data
        var prevData = e.prevData; // previous data (before this event)

        var schema = e.schema; // current schema
        var prevSchema = e.prevSchema; // previous schema (before this event)

        var selectedCategory = data.category;

        if (!selectedCategory) {
            /* no category selected yet, exit the function */
            return;
        }

        if (selectedCategory === prevData.category) {
            /* category hasn't changed, no need to update choices */
            return;
        }

        schema.keys.vehicle.choices = vehicleChoiceMap[selectedCategory];
        schema.keys.vehicle.helpText = "Select " + selectedCategory + " vehicle";
        data.vehicle = ''; // reset previously selected vehicle

        form.update({
            schema: schema,
            data: data
        })
    }


Loading your custom JS file on the admin page
---------------------------------------------

You can use the ``Media`` class to load your custom JS files in the admin page.

Quickest way is via your admin class:

.. code-block:: python

    # models.py

    class MyAdmin(admin.ModelAdmin):
        ...
        class Media:
            js = ('path/to/my-script.js',)

There are other ways as well (and perhaps more suitable in certain cases) for loading your
custom files, such as by subclassing the widget.

.. seealso::

    `Form Assets (the Media class) <https://docs.djangoproject.com/en/4.1/topics/forms/media/>`__
        Django's documentation on the ``Media`` class.
