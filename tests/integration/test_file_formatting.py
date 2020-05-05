###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from unittest import mock, skip

from approvaltests.approvals import verify
from io import StringIO

from cmake_tidy.formatting import SettingsReader
from tests.integration.test_integration_base import TestIntegrationBase
from tests.integration.utils import execute_cmake_tidy, normalize, get_input_file


class TestFileFormatting(TestIntegrationBase):
    def setUp(self):
        super(TestFileFormatting, self).setUp()
        self.fake_settings = SettingsReader.get_default_format_settings()

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
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_format_against_newline_violations_with_custom_settings(self, load_settings, stdout):
        self.fake_settings['succeeding_newlines'] = 4
        load_settings.return_value = self.fake_settings

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
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_format_indentation_when_spaces_after_command_name_are_present(self, load_settings, stdout):
        self.fake_settings['space_between_command_and_begin_parentheses'] = True
        load_settings.return_value = self.fake_settings

        self.format_file('indentations.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_format_line_splitting(self, load_settings, stdout):
        self.fake_settings['wrap_short_invocations_to_single_line'] = True
        load_settings.return_value = self.fake_settings

        self.format_file('line_length_handling.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_formatting_with_tabs(self, load_settings, stdout):
        self.fake_settings['tabs_as_spaces'] = False
        load_settings.return_value = self.fake_settings

        self.format_file('line_length_handling.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    def format_file(self, file: str):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=[get_input_file(file)]))

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_formatting_file_with_multiple_settings(self, load_settings, stdout):
        self.fake_settings['tabs_as_spaces'] = False
        self.fake_settings['keywords'] = ['GROUP']
        load_settings.return_value = self.fake_settings

        self.format_file('target_setting.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_formatting_of_install_commands(self, load_settings, stdout):
        self.fake_settings['tabs_as_spaces'] = False
        self.fake_settings['closing_parentheses_in_newline_when_split'] = True
        self.fake_settings['wrap_short_invocations_to_single_line'] = True
        self.fake_settings['keyword_and_single_value_in_one_line'] = True
        load_settings.return_value = self.fake_settings

        self.format_file('install.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_formatting_complicated_conditions(self, load_settings, stdout):
        self.fake_settings['tabs_as_spaces'] = False
        self.fake_settings['wrap_short_invocations_to_single_line'] = True
        load_settings.return_value = self.fake_settings

        self.format_file('complicated_conditions.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_formatting_complicated_conditions_splitting_after_operator(self, load_settings, stdout):
        self.fake_settings['tabs_as_spaces'] = False
        self.fake_settings['wrap_short_invocations_to_single_line'] = True
        self.fake_settings['condition_splitting_move_and_or_to_newline'] = False
        load_settings.return_value = self.fake_settings

        self.format_file('complicated_conditions.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_real_implementation_of_feature_in_cmake(self, load_settings, stdout):
        self.fake_settings['tabs_as_spaces'] = False
        self.fake_settings['closing_parentheses_in_newline_when_split'] = True
        self.fake_settings['wrap_short_invocations_to_single_line'] = True
        self.fake_settings['keyword_and_single_value_in_one_line'] = True
        load_settings.return_value = self.fake_settings

        self.format_file('set_of_functions.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @skip("New handling needed to enable this failing test")
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('cmake_tidy.commands.format.format_command.try_read_settings')
    def test_handling_of_single_line_comments_within_different_parts_of_cmake_file(self, load_settings, stdout):
        self.fake_settings['wrap_short_invocations_to_single_line'] = True
        self.fake_settings['keyword_and_single_value_in_one_line'] = True
        load_settings.return_value = self.fake_settings

        self.format_file('comments.cmake')

        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)
