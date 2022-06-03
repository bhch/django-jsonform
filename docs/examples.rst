Examples
========

Here are some schema examples to achieve fairly complex data structures.

Menu
----

This example shows how you can use JSON to store menu items for your website.

First let's look at the expected data structure:

.. code-block:: javascript

    // Data (javascript/json)
    [
        {'label': 'Home', 'link': '/', 'new_tab': false},
        {'label': 'About', 'link': '/about/', 'new_tab': false},
        {'label': 'Twitter', 'link': 'https://twitter.com/', 'new_tab': true},
    ]


And here's the corresponding schema for obtaining the above data:


.. code-block:: python

    # Schema
    {
        'type': 'list',
        'items': {
            'type': 'dict',
            'keys': {
                'label': {
                    'type': 'string'
                },
                'link': {
                    'type': 'string'
                },
                'new_tab': {
                    'type': 'boolean',
                    'title': 'Open in new tab'
                }
            }
        }
    }


Menu with nested items
----------------------

A menu item can either be a link or a dropdown containing multiple links as its children.

You can recursively nest an object within itself using the ``$ref`` keyword. See docs
on :ref:`referencing schema` for details:

.. code-block:: python
    :emphasize-lines: 17, 18, 19

    # Schema
    {
        'type': 'list',
        'items': {
            'type': 'dict',
            'keys': {
                'label': {
                    'type': 'string'
                },
                'link': {
                    'type': 'string'
                },
                'new_tab': {
                    'type': 'boolean',
                    'title': 'Open in new tab'
                },
                'children': {
                    '$ref': '#'
                }
            }
        }
    }


Image slider
------------

This example shows you how you can store an image slider in JSON.

First, let's look at the expected data structure:

.. code-block:: javascript

    // Data (javascript/json)
    [
        {
            'image': 'images/slide-1.png', 
            'heading': 'This is slide 1', 
            'caption': 'This is a caption',
            'button': {
                'label': 'Sign up',
                'link': '/sign-up/'
            }
        },
        {
            'image': 'images/slide-2.png', 
            'heading': 'This is slide 2', 
            'caption': 'This is another caption',
            'button': {
                'label': 'Learn more',
                'link': '/learn-more/'
            }
        }
    ]


And here's the corresponding schema for obtaining the above data:


.. code-block:: python

    # Schema
    {
        'type': 'list',
        'items': {
            'type': 'dict',
            'keys': {
                'image': {
                    'type': 'string',
                    'format': 'file-url'
                },
                'heading': {
                    'type': 'string'
                },
                'caption': {
                    'type': 'string'
                },
                'button': {
                    'type': 'object',
                    'keys': {
                        'label': {
                            'type': 'string'
                        },
                        'link': {
                            'type': 'string'
                        }
                    }
                }
            }
        }
    }
