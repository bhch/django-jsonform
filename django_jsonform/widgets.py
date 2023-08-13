import copy
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

    def get_schema(self):
        """Returns the schema attached to this widget.

        If the schema is a callable, it will return the result of the callable.
        """
        if callable(self.schema):
            if hasattr(self, 'instance') and len(signature(self.schema).parameters):
                schema = self.schema(self.instance)
            else:
                schema = self.schema()
        else:
            schema = self.schema

        return schema

    def render(self, name, value, attrs=None, renderer=None):
        schema = normalize_schema(self.get_schema())

        context = self.get_context(name, value, attrs)

        context['widget'].update({
            'config': {
                'data': value or json.dumps(''),
                'schema': schema,
                'fileHandler': self.file_handler or get_setting('FILE_HANDLER', ''),
                'fileHandlerArgs': {
                    'field_name': context['widget']['name'],
                    'model_name': self.model_name,
                },
                'errorMap': getattr(self, 'error_map', {}),
                'validateOnSubmit': self.validate_on_submit,
                'readonly': attrs.get('disabled', False),
            },
        })

        # backwards compatibility for `JSONFORM_UPLOAD_HANDLER` setting
        if not context['widget']['config']['fileHandler']:
            try:
                context['widget']['config']['fileHandler'] = reverse('django_jsonform:upload')
            except NoReverseMatch:
                pass

        # Turn widget config into json string
        context['widget']['config'] = json.dumps(context['widget']['config'])

        return mark_safe(render_to_string(self.template_name, context))

    def add_error(self, error_map):
        if not hasattr(self, 'error_map'):
            setattr(self, 'error_map', copy.deepcopy(error_map))
            return

        # if here, this is being called more than once
        # therefore, extend the current error_map
        for key in error_map:
            if key in self.error_map:
                if not isinstance(self.error_map[key], list):
                    self.error_map[key] = [self.error_map[key]]
                if isinstance(error_map[key], list):
                    self.error_map[key] += error_map[key]
                else:
                    self.error_map[key].append(error_map[key])
            else:
                self.error_map[key] = error_map[key]

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
            'django_jsonform/index.js',
        ]

        return forms.Media(css=css, js=js)
