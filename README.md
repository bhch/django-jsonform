<p align="center">
  <img src="https://raw.githubusercontent.com/bhch/django-jsonform/master/docs/_static/logo.png" width="200" alt="django-jsonform icon">
</p>

<p align="center">
    A user-friendly JSON editing form for django admin.
</p>

<p align="center">
    <a href="http://django-jsonform.rtfd.io">Documentation</a> &bull;
    <code>Django &gt;= 2.0</code>
</p>

## Features

 - [x] File uploads
 - [x] Postgres `ArrayField`
 - [x] Many inputs and field types
 - [x] UI matches with Django admin's
 - [ ] Validation
 - [ ] Recursion (nesting with self references)

## Screenshots

Here's a screenshot of items being added to a shopping list (JSON array) dynamically:

![django-jsonform screenshot](https://raw.githubusercontent.com/bhch/django-jsonform/master/docs/_static/quickstart.gif)

## Install

Install via pip:

```sh
$ pip install django-jsonform
```

Edit your *settings.py* file:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'django_jsonform'
]
```

## Upgrading notes

When upgrading from an older version of this library, please ensure that your
browser is loading the latest static JavaScript files that come with this library.

 - In the development environment, clear the browser cache.
 - In the production environment, you must run the `collectstatic` command to update
 the static files.

## Documentation

Quickstart and usage docs can be found at [http://django-jsonform.rtfd.io](http://django-jsonform.rtfd.io).


## License

[BSD-3-Clause](LICENSE.txt)

---

If you've found this library useful, and if you wish to support me you can:

<a href="https://www.buymeacoffee.com/bhch">
    <img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg" width="170">
</a>
