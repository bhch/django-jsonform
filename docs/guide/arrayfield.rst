Using with Postgres ``ArrayField``
==================================

django-jsonform provides a custom :class:`~django_jsonform.models.fields.ArrayField`
class which renders a dynamic form input.

It is a subclass of Django's ``ArrayField`` and the usage api is exactly the same.

.. code-block:: python

    from django_jsonform.models.fields import ArrayField


    class MyModel(models.Model):
        items = ArrayField(models.CharField(max_length=50), size=10)