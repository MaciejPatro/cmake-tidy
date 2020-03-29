###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from unittest import mock

from approvaltests.approvals import verify
from io import StringIO

from tests.integration.test_integration_base import TestIntegrationBase
from tests.integration.utils import execute_cmake_tidy, normalize, get_input_file


class TestCMakeTidyFormat(TestIntegrationBase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_command_help_shown(self, stdout):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--help']))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_incorrect_command_should_print_error_with_usage_help(self, stdout):
        self.assertFail(execute_cmake_tidy(command='format', arguments=[]))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_config_only_configuration_to_stdout_by_default(self, stdout):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config', 'dummy.txt']))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('cmake_tidy.formatting.settings_reader.SettingsReader._read_settings',
                mock.MagicMock(return_value={'tabs_as_spaces': False}))
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_full_config_even_if_file_overrides_only_one(self, stdout):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config', 'file.txt']))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('cmake_tidy.commands.format.output_writer.OutputWriter.write')
    def test_format_inplace_simple_file(self, write):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['-i', get_input_file('arguments.cmake')]))
        write.assert_called_once()
        normalized_output = normalize(write.call_args[0][0])
        verify(normalized_output, self.reporter)

    @mock.patch('cmake_tidy.formatting.settings_reader.SettingsReader._read_settings',
                mock.MagicMock(return_value={'tabs_as_spaces': 33}))
    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_format_should_fail_with_warning_about_incorrect_settings_when_dump_invoked(self, stdout):
        self.assertFail(execute_cmake_tidy(command='format', arguments=['--dump-config', 'file.txt']))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('cmake_tidy.formatting.settings_reader.SettingsReader._read_settings',
                mock.MagicMock(return_value={'tabs_as_spaces': 33}))
    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_format_should_fail_with_warning_about_incorrect_settings_when_trying_to_format(self, stdout):
        self.assertFail(execute_cmake_tidy(command='format', arguments=[get_input_file('arguments.cmake')]))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)
