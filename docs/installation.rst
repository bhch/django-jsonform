Installation
============

Requirements:

- Python >= 3.4
- Django >= 2.0

Install using pip:

.. code-block:: sh

    $ pip install django-jsonform


We also upload `pre-built packages <https://github.com/bhch/django-jsonform/releases>`_
on Github in case pip or PyPI server isn't working.


Update your project's settings:

.. code-block:: python

    # settings.py
    
    INSTALLED_APPS = [
        # ...
        'django_jsonform'
    ]


.. admonition:: Upgrading notes
    
    When upgrading from an older version of this library, please ensure that your
    browser is loading the latest static JavaScript files that come with this library:

    - In the development environment, clear the browser cache.
    - In the production environment, you must run the ``collectstatic`` command to update
      the static files.


Next, go to :doc:`quickstart` page for basic usage instructions.