import django
from django.conf import settings

if django.VERSION[0] >= 3 and django.VERSION[1] >= 1:
    # Django >= 3.1
    from django.db.models import JSONField as DjangoJSONField
else:
    # Django < 3.1
    if 'postgres' in settings.DATABASES['default']['ENGINE']:
        from django.contrib.postgres.fields import JSONField as DjangoJSONField
    else:
        from django_jsonform.models.compat import JSONField as DjangoJSONField

from django.contrib.postgres.fields import ArrayField as DjangoArrayField
from django_jsonform.forms.fields import JSONFormField
from django_jsonform.forms.fields import ArrayFormField


class JSONField(DjangoJSONField):
    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop('schema', {})
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': JSONFormField,
            'schema': self.schema,
            'model_name': self.model.__name__,
            **kwargs
        })


class ArrayField(DjangoArrayField):
    def __init__(self, *args, **kwargs):
        self.nested = kwargs.pop('nested', False)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{'form_class': ArrayFormField, 'nested': self.nested, **kwargs})