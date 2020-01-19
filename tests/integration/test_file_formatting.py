from unittest import mock

from approvaltests.approvals import verify
from io import StringIO

from cmake_tidy.formatting import _get_default_format_settings
from tests.integration.test_integration_base import TestIntegrationBase
from tests.integration.utils import execute_cmake_tidy, normalize, get_input_file


class TestFileFormatting(TestIntegrationBase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_command_should_print_file_to_output(self, stdout):
        self.format_file('first_example.cmake')
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_against_newline_violations(self, stdout):
        self.format_file('newlines_violations.cmake')
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.load_format_settings')
    def test_format_against_newline_violations_with_custom_settings(self, load_settings, stdout):
        fake_settings = _get_default_format_settings()
        fake_settings['succeeding_newlines'] = 4
        load_settings.return_value = fake_settings

        self.format_file('newlines_violations.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_tabs_with_spaces_replacement(self, stdout):
        self.format_file('spaces_violations.cmake')
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_bracket_arguments_handling(self, stdout):
        self.format_file('arguments.cmake')
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_indentation_of_basic_invocations(self, stdout):
        self.format_file('indentations.cmake')
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.load_format_settings')
    def test_format_indentation_when_spaces_after_command_name_are_present(self, load_settings, stdout):
        fake_settings = _get_default_format_settings()
        fake_settings['space_between_command_and_begin_parentheses'] = True
        load_settings.return_value = fake_settings

        self.format_file('indentations.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    def format_file(self, file: str):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=[get_input_file(file)]))