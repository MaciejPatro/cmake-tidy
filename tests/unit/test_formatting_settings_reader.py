from unittest import mock, TestCase

from cmake_tidy.formatting.settings_reader import InvalidSchemaError, SettingsReader, SchemaValidationError


class TestSettingReader(TestCase):
    @mock.patch('cmake_tidy.formatting.settings_reader.SettingsReader._read_schema_file',
                return_value={'description', 'type'})
    def test_settings_reader_construction_should_raise_when_schema_is_invalid(self, read_schema_file):
        with self.assertRaises(InvalidSchemaError):
            SettingsReader()

    def test_settings_reader_current_schema_should_be_correct(self):
        try:
            SettingsReader()
        except InvalidSchemaError:
            self.fail()

    @mock.patch('cmake_tidy.formatting.settings_reader.SettingsReader._read_settings',
                return_value={'random': 1})
    def test_invalid_settings_data_provided(self, read_settings):
        self.assertSchemaValidationFails()

    @mock.patch('cmake_tidy.formatting.settings_reader.SettingsReader._read_settings',
                return_value={'line_length': True})
    def test_valid_setting_name_with_wrong_value_type(self, read_settings):
        self.assertSchemaValidationFails()

    @mock.patch('cmake_tidy.formatting.settings_reader.SettingsReader._read_settings')
    def test_default_settings_should_be_valid(self, read_settings):
        read_settings.return_value = SettingsReader.get_default_format_settings()
        try:
            SettingsReader().try_loading_format_settings()
        except SchemaValidationError:
            self.fail()

    def assertSchemaValidationFails(self):
        with self.assertRaises(SchemaValidationError):
            SettingsReader().try_loading_format_settings()
