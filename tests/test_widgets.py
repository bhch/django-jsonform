from unittest import TestCase
from unittest.mock import MagicMock
from django_jsonform.widgets import JSONFormWidget


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

    def test_instance_arg_is_conditionally_passed_to_schema_callable(self):
        """The 'instance' argument must be conditionally passed
        to the schema function, i.e. only if it accepts arguments.
        This is to ensure backwards compatibility.
        """

        schema_func = lambda: {} # accepts no args

        widget = JSONFormWidget(schema=schema_func)
        widget.instance = 1
        # must not raise any exceptions
        widget.render(name='test', value='')

    def test_merges_error_maps(self):
        """error_map must be merged with the previously passed error_maps"""
        widget = JSONFormWidget(schema={})

        error_map = {'0': 'First error'}
        widget.add_error(error_map)

        error_map_2 = {'0': 'Second error'}
        widget.add_error(error_map_2)

        error_map_3 = {'0': ['Third error']} # if messages are in array
        widget.add_error(error_map_3)

        self.assertEqual(
            widget.error_map['0'],
            ['First error', 'Second error', 'Third error']
        )
