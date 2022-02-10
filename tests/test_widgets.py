from unittest import TestCase
from unittest.mock import MagicMock
from django_jsonform.widgets import JSONFormWidget


def dynamic_schema_accepts_args(instance=None):
    return {}


def dynamic_schema_no_args():
    return {}


class JSONFormWidgetTests(TestCase):
    def test_passes_model_instance_to_schema_callable(self):
        """If an 'instance' attribute was set on the widget,
        it should be passed to the schema function in the
        widget's render method.
        """

        schema_func = MagicMock(return_value={})

        widget = JSONFormWidget(schema=schema_func)
        widget.render(name='test', value='')
        # no 'instance' attribute set,
        # nothing should be passed to callable
        schema_func.assert_called_with()

        widget.instance = 1 # set instance
        widget.render(name='test', value='')
        # 'instance' attribute set,
        # must be passed to callable
        schema_func.assert_called_with(1)

    def test_maintains_backwards_compatibility(self):
        """The 'instance' argument must be conditionally passed
        to the schema function, i.e. only if it accepts arguments.
        """

        schema_func = lambda: {} # accepts no args

        widget = JSONFormWidget(schema=schema_func)
        widget.instance = 1
        # must not raise any exceptions
        widget.render(name='test', value='')
