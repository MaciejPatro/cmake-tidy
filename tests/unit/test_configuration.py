import unittest

from cmake_tidy.configuration import Configuration


class TestConfigurationPropertiesHandling(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Configuration({})

    def test_input_should_be_empty_when_no_file_specified(self):
        self.assertEqual('', self.config.input)

    def test_not_existing_property_should_raise(self):
        with self.assertRaises(AttributeError):
            self.config.some

    def test_all_properties_should_not_contain_key_with_same_name(self):
        self.assertNotIn('all_properties', self.config.all_properties)

     
class TestConfigurationInheritanceBehavior(unittest.TestCase):
    class InheritedConfiguration(Configuration):
        def __init__(self, arguments: dict):
            super().__init__(arguments)
            
        @property
        def new_property(self):
            return 'new'

        @property
        def initialized_property(self):
            return self._config.get(self._property_name())

    def setUp(self) -> None:
        self.inherited_config = self.InheritedConfiguration({'initialized_property': 'abc'})

    def test_should_contain_main_class_property(self):
        self.assertEqual('', self.inherited_config.input)

    def test_should_have_new_property_setup(self):
        self.assertEqual('new', self.inherited_config.new_property)

    def test_should_initialize_correctly_inherited_property(self):
        self.assertEqual('abc', self.inherited_config.initialized_property)

    def test_all_properties_should_contain_also_inherited_ones(self):
        self.assertIn('new_property', self.inherited_config.all_properties)
