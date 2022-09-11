import json
from inspect import signature
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_jsonform.utils import normalize_schema, get_setting
from django.urls import reverse, NoReverseMatch


class JSONFormWidget(forms.Widget):
    template_name = 'django_jsonform/editor.html'

    def __init__(
        self,
        schema,
        model_name='',
        file_handler='',
        validate_on_submit=False,
        attrs=None,
    ):
        super().__init__(attrs=attrs)

        self.schema = schema
        self.model_name = model_name
        self.file_handler = file_handler
        self.validate_on_submit = validate_on_submit


    def render(self, name, value, attrs=None, renderer=None):
        if callable(self.schema):
            if hasattr(self, 'instance') and len(signature(self.schema).parameters):
                schema = self.schema(self.instance)
            else:
                schema = self.schema()
        else:
            schema = self.schema

        schema = normalize_schema(schema)

        context = self.get_context(name, value, attrs)

        context['widget'].update({
            'model_name': self.model_name,
            'data': value or json.dumps(''),
            'schema': json.dumps(schema),
            'file_handler': self.file_handler or get_setting('FILE_HANDLER', ''),
            'error_map': getattr(self, 'error_map', {}),
            'validate_on_submit': self.validate_on_submit
        })

        # backwards compatibility for `JSONFORM_UPLOAD_HANDLER` setting
        if not context['widget']['file_handler']:
            try:
                context['widget']['file_handler'] = reverse('django_jsonform:upload')
            except NoReverseMatch:
                pass

        return mark_safe(render_to_string(self.template_name, context))

    def add_error(self, error_map):
        setattr(self, 'error_map', json.dumps(error_map))

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
