Uploading files
=============== 

There are two ways to keep files in a JSON data:

1. Base64 string - the file will be encoded as Base64 string and all the data
   will be kept within the JSON object.
2. File url - the file will be uploaded on the server and only the URL of the file
   will be kept in the JSON object.


Base64 string
-------------

This option is ideal for keeping small file data within a JSON object.

However, there are two drawbacks: Base64 encoded data will be 33% larger than
the original file. Second, Base64 images and files won't be cached by the browsers
unlike other images accessed via urls.

The ``type`` should be ``string`` and ``format`` should be ``'data-url'``:

.. code-block:: python

    # Schema
    {
        'type': 'object',
        'keys': {
            'logo': {
                'type': 'string',
                'format': 'data-url'
            }
        }
    }


    # Output data
    {
        'logo': 'data:image/png;base64,<long-base64-encoded-data>'
    }



File url
--------

This option is ideal for keeping large files.

However, it requires a little more work to set up.

Since the files will be sent to the server, you will have to create an
upload handler function which will be responsible for saving the files and
returning the file's url.

A handler function is similar to a view: it receives a ``request`` object as a
parameter. **But** instead of returning an HTTP response, it returns the name
of the newly created file.

A sample handler function:

.. code-block:: python

    # views.py

    def upload_handler(request):
        file = request.FILES[0]

        # you can save the file however you want:
        # (i) write it directly to the filesystem,
        # (ii) or keep it in a separate model.

        # In this example, we'll save it in a
        # dedicated model for storing files

        obj = MediaModel(file=file)
        obj.save()

        # return the path of the file
        # this value will be kept in the JSON data
        return obj.file.name


.. attention::

    It is recommended your upload handler function should **return the path**
    of the uploaded file **without the media url prefix**.

    The rationale behind it is that file's url may change but file's name
    and path doesn't.

    If you're keeping the files in the ``media`` directory, the url of that file
    will look like: ``/media/path/to/image.png``.

    But if later you wish to migrate your files to a third party service such as
    AWS S3 bucket. Then the file's url will be completely different:
    ``https://s3-bucketname.amazonaws.com/path/to/image.png``.

    If you save the full url in the JSON data, then that value won't be updated
    and still have the old url.

    A better way is to just keep the path of the file and use Django's
    ``{% get_media_prefix %}`` tag in the templates to create the full url.

    See :ref:`Accessing files in templates` section below for more.


Now, you need to declare this upload handler function in the settings file:

.. code-block:: python

    # settings.py

    JSONFORM_UPLOAD_HANDLER = 'myapp.views.upload_handler'


Finally, you also need to include ``django-jsonform``'s urls in your main urls.py
file:

.. code-block:: python

    # project's main urls.py

    from django.urls import path, include

    urlpatterns = [
        # ...
        path('django-jsonform/', include('django_jsonform.urls')),
        # ...
    ]


Behind the scenes, django-jsonform will send an AJAX request to
``/django-jsonform/upload/`` url and your handler function will be called with the
request.


You're all set now to upload files.

In the schema, the ``type`` should be ``string`` and ``format`` should be ``'file-url'``:

.. code-block:: python

    # Schema
    {
        'type': 'object',
        'keys': {
            'logo': {
                'type': 'string',
                'format': 'file-url'
            }
        }
    }


    # Output data
    {
        'logo': 'path/to/logo.png'
    }


.. _file-upload-request-parameters:

Additional request parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases, you may want to know the name of the model or name of the field
while saving the file.

The ``request.POST`` will have keys named ``model_name`` and ``field_name`` present.

However, the widget has no way of knowing the name of the model, so you'll have
to pass it to the widget while initializing:

.. code-block:: python

    JSONFormWidget(schema=schema, model_name='MyModel')

In your upload handler, you can access the additional parameters like this:

.. code-block:: python

    def upload_handler(request):
        file = request.FILES[0]

        model_name = request.POST['model_name']
        field_name = request.POST['field_name']
    

Accessing files in templates
----------------------------

For ``data-url``, you can just use the value as it is.

For ``file url``, you may want to prepend a media url prefix using Django's
``{% get_media_prefix %}`` tag (`see Django docs <https://docs.djangoproject.com/en/3.2/ref/templates/builtins/#get-media-prefix>`_).

Suppose the data looks like this:

.. code-block:: python

    # Sample data
    data = {
        'image': 'path/to/image.png'
    }

Then in the template, you'll do something like this:

.. code-block:: django

    {% load static %}

    <img src="{% get_media_prefix %}{{ data.image }}">