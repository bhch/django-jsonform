<p align="center">
  <img src="https://raw.githubusercontent.com/bhch/django-jsonform/master/docs/_static/logo.png" width="200" alt="django-jsonform icon">
</p>

<p align="center">
    A user-friendly JSON editing form for django admin.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-%3E%3D%203.4-blue">
  <img src="https://img.shields.io/badge/Django-%3E%3D%202.0-blue">
  <img src="https://img.shields.io/pypi/dm/django-jsonform">
</p>

<p align="center">
  <strong><a href="https://django-jsonform.rtfd.io">Documentation</a></strong> &bull;
  <strong><a href="https://bhch.github.io/react-json-form/playground/">Playground</a></strong> &bull;
  <strong><a href="https://pypi.org/project/django-jsonform/">PyPI</a></strong>
</p>

## Features

 - [x] File uploads
 - [x] Postgres `ArrayField`
 - [x] Many inputs and field types
 - [x] UI matches with Django admin's
 - [x] Recursion (nesting with self references)
 - [ ] Validation

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

## Contributing

 - The JavaScript code is written in React and it lives in another repo: https://github.com/bhch/react-json-form.  
   The JS code lacks proper documentation or comments, so before contributing, maybe open an issue and I can help you out.
 - For everything else (related to Django or widget's css), contribute directly to this repo.

## License

[BSD-3-Clause](LICENSE.txt)
