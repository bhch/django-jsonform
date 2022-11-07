import pkg_resources
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if pkg_resources.parse_version(django.get_version()) >= pkg_resources.parse_version("3.1"):
    # Django >= 3.1
    from django.db.models import JSONField as DjangoJSONField
else:
    # Django < 3.1
    if 'postgres' in settings.DATABASES['default']['ENGINE']:
        from django.contrib.postgres.fields import JSONField as DjangoJSONField
    else:
        from django_jsonform.models.compat import JSONField as DjangoJSONField

try:
    from django.contrib.postgres.fields import ArrayField as DjangoArrayField
except ImportError:
    class DjangoArrayField:
        mock_field = True

from django_jsonform.forms.fields import JSONFormField
from django_jsonform.forms.fields import ArrayFormField


class JSONField(DjangoJSONField):
    form_class = JSONFormField

    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop('schema', {})
        self.pre_save_hook = kwargs.pop('pre_save_hook', None)
        self.file_handler = kwargs.pop('file_handler', '')
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': self.form_class,
            'schema': self.schema,
            'model_name': self.model.__name__,
            'file_handler': self.file_handler,
            **kwargs
        })

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)

        if (self.pre_save_hook):
            value = self.pre_save_hook(value)

        return value


class ArrayField(DjangoArrayField):
    form_class = ArrayFormField

    def __init__(self, *args, **kwargs):
        if hasattr(DjangoArrayField, 'mock_field'):
            raise ImproperlyConfigured('ArrayField requires psycopg2 to be installed.')

        self.nested = kwargs.pop('nested', False)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{'form_class': self.form_class, 'nested': self.nested, **kwargs})
