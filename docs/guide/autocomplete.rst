Autocomplete widget
===================

.. versionadded:: 2.12

The autocomplete widget can be used for fetching options from the server via AJAX
requests.

**Here's an animated GIF of the autocomplete widget:**

.. image:: /_static/autocomplete.gif
    :alt: Animated screenshot of autocomplete widget.

Usage:

.. code-block:: python
    :emphasize-lines: 5,6

    # Schema

    {
        'type': 'string',
        'widget': 'autocomplete',
        'handler': '/url/to/handler_view' # hard-coded url

        # OR

        'handler': reverse_lazy('handler-view-name') # reversed URL
    }



The ``handler`` keyword declares the URL of the view which will handle the AJAX
requests.

You can use ``django.urls.reverse_lazy`` instead of hard-coding the handler url.


Multiselect + Autocomplete
--------------------------

.. vsersionadded:: 2.20

You can use ``"widget": "multiselect-autocomplete"`` to get an autocomplete input
with multiple selections.


Handling AJAX requests
----------------------

Your handler view will receive a ``GET`` request with a ``query`` parameter
containing the search term typed in the autocomplete input.

Code example
~~~~~~~~~~~~

.. code-block:: python

    from django.http import JsonResponse
    from django.contrib.auth.decorators import login_required

    @login_required
    def autocomplete_handler(request):
        query = request.GET.get('query') # search query

        # ... do something ...

        results = [
            'Australia',
            'Brazil',
        ]

        return JsonResponse({'results': results})


Request arguments
~~~~~~~~~~~~~~~~~

Each ``GET`` request will contain these parameters:

- ``query``: Search term typed in the autocomplete input.
- ``model_name``: Name of the model.
- ``field_name``: Name of the field.
- ``coords``: :doc:`Coordinates </guide/coordinates>` of the data input field.

Response format
~~~~~~~~~~~~~~~

Your view must return a ``JsonResponse`` in this format:

.. code-block:: python

    JsonResponse({'results': ['Australia', 'Brazil', ...]})

The options can also have different display label and value:

.. code-block:: python
    
    JsonResponse({
        'results': [
            {'title': 'Australia', 'value': 'AU'},
            {'title': 'Brazil', 'value': 'BR'},
            ...
        ]
    })
