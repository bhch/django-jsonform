Settings
========

This documents lists the settings which can be used to configure django-jsonform's
behaviour.

.. setting:: DJANGO_JSONFORM

``DJANGO_JSONFORM``
-------------------

.. versionadded:: 2.11

This is the main "wrapper" setting to hold all django-jsonform specific settings.

Defaults:

.. code-block:: python

    DJANGO_JSONFORM = {
        'FILE_HANDLER': ''
    }


All the following documented settings are keys of the main :setting:`DJANGO_JSONFORM`
setting dict.


.. setting:: FILE_HANDLER

``FILE_HANDLER``
~~~~~~~~~~~~~~~~

Default: ``''`` (Empty string)

URL to the file handler view. Example: ``'/json-file-handler/'``.

Use this setting to declare a common file handler function for all ``JSONField`` instances.
All the file upload and listing requests will be sent to this URL.

----

``JSONFORM_UPLOAD_HANDLER``
---------------------------

.. deprecated:: 2.11

This setting was used for declaring the file upload handler function.

It is only kept for backwards compatibility. It will be removed in future.
