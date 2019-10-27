import unittest
import mock

from approvaltests.approvals import verify
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
from io import StringIO

from cmake_tidy.formatting import _get_default_format_settings
from tests.integration.utils import execute_cmake_tidy, normalize


class TestCMakeTidyFormat(unittest.TestCase):
    def setUp(self):
        self.reporter = GenericDiffReporterFactory().get_first_working()

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_command_help_shown(self, stdout):
        execute_cmake_tidy(command='format', arguments=['--help'])
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_incorrect_command_should_print_error_with_usage_help(self, stdout):
        execute_cmake_tidy(command='', arguments=[])
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_command_should_print_file_to_output(self, stdout):
        execute_cmake_tidy(command='format', arguments=['input_files/first_example.cmake'])
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_against_newline_violations(self, stdout):
        execute_cmake_tidy(command='format', arguments=['input_files/newlines_violations.cmake'])
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.command_line_handling.format_command.load_format_settings')
    def test_format_against_newline_violations_with_custom_settings(self, load_settings, stdout):
        fake_settings = _get_default_format_settings()
        fake_settings['succeeding_newlines'] = 4
        load_settings.return_value = fake_settings

        execute_cmake_tidy(command='format', arguments=['input_files/newlines_violations.cmake'])

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_tabs_with_spaces_replacement(self, stdout):
        execute_cmake_tidy(command='format', arguments=['input_files/spaces_violations.cmake'])
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_bracket_arguments_handling(self, stdout):
        execute_cmake_tidy(command='format', arguments=['input_files/arguments.cmake'])
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)
