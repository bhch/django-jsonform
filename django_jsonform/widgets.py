import json
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_jsonform.utils import normalize_schema


class JSONFormWidget(forms.Widget):
    template_name = 'django_jsonform/editor.html'

    def __init__(self, schema, model_name=''):
        super().__init__()

        self.schema = schema
        self.model_name = model_name

    def render(self, name, value, attrs=None, renderer=None):
        if callable(self.schema):
            schema = self.schema()
        else:
            schema = self.schema

        schema = normalize_schema(schema)

        context = {
            'name': name,
            'model_name': self.model_name,
            'data': value or json.dumps(''),
            'schema': json.dumps(schema),
        }
        return mark_safe(render_to_string(self.template_name, context))

    @property
    def media(self):
        css = {
            'all': [
                'django_jsonform/style.css',
            ]
        }
        js = [
            'django_jsonform/vendor/react.production.min.js',
            'django_jsonform/vendor/react-dom.production.min.js',
            'django_jsonform/react-json-form.min.js',
        ]

        return forms.Media(css=css, js=js)
