import unittest

from cmake_tidy.formatting import CMakeFormatter
from tests.unit.parser_composite_elements import spaces, newlines, command_invocation, line_ending, unhandled, file


class TestCMakeFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.__settings = {'succeeding_newlines': 1, 'tab_size': 2}

    def test_return_single_newline(self):
        self.assertFormatting('\n', newlines(3))

    def test_return_3_newlines_although_settings_allow_more(self):
        self.__settings['succeeding_newlines'] = 5
        self.assertFormatting('\n\n\n', newlines(3))

    def test_replace_tab_with_space_one_to_two(self):
        self.assertFormatting(' ' * 4, spaces('\t\t'))

    def test_replace_tabs_with_multiple_spaces(self):
        self.__settings['tab_size'] = 4
        self.assertFormatting(' ' * 10, spaces(' \t \t'))

    @unittest.SkipTest
    def test_function_should_force_indentation_for_command_invocation_and_line_comments_only(self):
        function_with_invocation_in_second_line = command_invocation('function(') \
            .add(newlines(1)) \
            .add(line_ending('# comment', 1)) \
            .add(unhandled('abc')) \
            .add(newlines(1)) \
            .add(command_invocation('test('))

        expected_formatting = """function()
  # comment
abc
  test()"""
        self.assertFormatting(expected_formatting, function_with_invocation_in_second_line)

    def test_function_declaration_should_indent_correctly_within_its_scope(self):
        function_with_invocation_in_second_line = file() \
            .add(command_invocation('function(')) \
            .add(newlines(1)) \
            .add(command_invocation('test(')) \
            .add(newlines(1)) \
            .add(command_invocation('endfunction(')) \
            .add(newlines(1)) \
            .add(command_invocation('test2('))
        expected_formatting = """function()
  test()
endfunction()
test2()"""
        self.assertFormatting(expected_formatting, function_with_invocation_in_second_line)

    def assertFormatting(self, formatted_string, lex_data):
        self.assertEqual(formatted_string, CMakeFormatter(self.__settings).format(lex_data))
