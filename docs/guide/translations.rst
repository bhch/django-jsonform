Lazy translations
=================

.. versionadded:: 2.7

You may want to display field labels or choice names in a particular user's local
language. For those cases, the schema also supports lazy translations:

.. code-block:: python

    from django.utils.translation import gettext_lazy as _


    {
        'type': 'string',
        'title': _('Occupation'),
        'choices': [
            {'value': 'teacher', 'title': _('Teacher')},
            {'value': 'doctor', 'title': _('Doctor')},
            {'value': 'engineer', 'title': _('Engineer')},
        'default': 'teacher'
    }
