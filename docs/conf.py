# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath("./_ext"))

from django_jsonform import __version__


# -- Project information -----------------------------------------------------

project = 'django-jsonform'
copyright = '2021 Bharat Chauhan'
author = 'Bharat Chauhan'

version = __version__

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.extlinks',
    'helpers',
]

add_module_names = False

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'logo_only': True,
}
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'
html_css_files = [
    'candy.css',
    # We load fonts directly in `layout.html` template because
    # specifying links here doesn't not allow for setting 
    # "preconnect" and "crossorigin" attributes on the tags.
]
html_show_sphinx = False
html_context = {
    'google_search_console_verification': '8Isauv2ltEzkMMhQeMjQedq39VQFeKa0sZXqnPEHpFg'
}

extlinks = {
    'issue': (
        'https://github.com/bhch/django-jsonform/issues/%s',
        '#' # verions 4+ also require '%s' in this value
    )
}
