import unittest

from cmake_tidy.formatting import CMakeFormatter
from tests.unit.parser_composite_elements import spaces, newlines, command_invocation


class TestCMakeFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.__settings = {'succeeding_newlines': 1, 'tab_size': 2}

    def test_return_single_newline(self):
        self.assert_formatting(newlines(3), '\n')

    def test_return_3_newlines_although_settings_allow_more(self):
        self.__settings['succeeding_newlines'] = 5
        self.assert_formatting(newlines(3), '\n\n\n')

    def test_replace_tab_with_space_one_to_two(self):
        self.assert_formatting(spaces('\t\t'), ' ' * 4)

    def test_replace_tabs_with_multiple_spaces(self):
        self.__settings['tab_size'] = 4
        self.assert_formatting(spaces(' \t \t'), ' ' * 10)

    @unittest.SkipTest
    def test_function_should_force_indentation_for_next_lines(self):
        function_with_invocation_in_second_line = command_invocation('function(') \
            .add(newlines(1)) \
            .add(command_invocation('test('))
        expected_formatting = 'function()\n  test()'

        f = CMakeFormatter(self.__settings)
        self.assertEqual(expected_formatting, f.format(function_with_invocation_in_second_line))

    def assert_formatting(self, lex_data, formatted_string):
        self.assertEqual(formatted_string, CMakeFormatter(self.__settings).format(lex_data))
