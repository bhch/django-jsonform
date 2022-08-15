import json
from inspect import signature
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_jsonform.utils import normalize_schema, get_setting
from django.urls import reverse, NoReverseMatch


class JSONFormWidget(forms.Widget):
    template_name = 'django_jsonform/editor.html'

    def __init__(self, schema, model_name='', file_handler=''):
        super().__init__()

        self.schema = schema
        self.model_name = model_name
        self.file_handler = file_handler

    def render(self, name, value, attrs=None, renderer=None):
        if callable(self.schema):
            if hasattr(self, 'instance') and len(signature(self.schema).parameters):
                schema = self.schema(self.instance)
            else:
                schema = self.schema()
        else:
            schema = self.schema

        schema = normalize_schema(schema)

        context = {
            'name': name,
            'model_name': self.model_name,
            'data': value or json.dumps(''),
            'schema': json.dumps(schema),
            'file_handler': self.file_handler or get_setting('FILE_HANDLER', ''),
        }

        # backwards compatibility for `JSONFORM_UPLOAD_HANDLER` setting
        if not context['file_handler']:
            try:
                context['file_handler'] = reverse('django_jsonform:upload')
            except NoReverseMatch:
                pass

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
            'django_jsonform/vendor/react-modal.min.js',
            'django_jsonform/react-json-form.js',
        ]

        return forms.Media(css=css, js=js)
