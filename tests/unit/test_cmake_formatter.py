###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest

from cmake_tidy.formatting import CMakeFormatter
from cmake_tidy.lexical_data.elements import Element
from tests.unit.parser_composite_elements import spaces, newlines, file, command_invocation


class TestCMakeFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = {'succeeding_newlines': 1,
                         'tab_size': 2,
                         'force_command_lowercase': True,
                         'wrap_short_invocations_to_single_line': False,
                         'closing_parentheses_in_newline_when_split': False,
                         'line_length': 80,
                         'keep_property_and_value_in_one_line': False,
                         'keyword_and_single_value_in_one_line': False,
                         'tabs_as_spaces': True}

    def assertFormatting(self, formatted_string, lex_data):
        self.assertEqual(formatted_string, CMakeFormatter(self.settings).format(lex_data))

    def assertFormattingArguments(self, expected_formatting, function_arguments):
        self.assertFormatting(expected_formatting, file().add(command_invocation('abc(', function_arguments)))

    def assertConditionFormatting(self, expected: str, args: Element):
        root = file().add(command_invocation('if(', args))
        self.assertFormatting(expected, root)


class TestCMakeFormatterBasicElements(TestCMakeFormatter):
    def test_return_single_newline(self):
        self.assertFormatting('\n', file().add(newlines(3)))

    def test_return_3_newlines_although_settings_allow_more(self):
        self.settings['succeeding_newlines'] = 5
        self.assertFormatting('\n\n\n', file().add(newlines(3)))

    def test_replace_tab_with_space_one_to_two(self):
        self.assertFormatting(' ' * 4, spaces('\t\t'))

    def test_replace_tabs_with_multiple_spaces(self):
        self.settings['tab_size'] = 4
        self.assertFormatting(' ' * 10, spaces(' \t \t'))
