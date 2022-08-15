from unittest import TestCase
from unittest.mock import MagicMock, patch
from django_jsonform.models.fields import JSONField


class JSONFieldTests(TestCase):
    def test_calls_pre_save_hook_if_provided(self):
        pre_save_hook = MagicMock(return_value={})
        field = JSONField(schema={}, pre_save_hook=pre_save_hook)
        field.attname = 'test'
        model_instance = MagicMock()
        field.pre_save(model_instance, True)
        pre_save_hook.assert_called_once()
