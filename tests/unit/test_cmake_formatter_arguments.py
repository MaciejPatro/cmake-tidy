import unittest

from tests.unit.parser_composite_elements import spaces, file, command_invocation, unquoted_argument, \
    arguments, quoted_argument, newlines
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandArguments(TestCMakeFormatter):
    def assertFormattingArguments(self, expected_formatting, function_arguments):
        self.assertFormatting(expected_formatting, file().add(command_invocation('abc(', function_arguments)))

    def test_no_spaces_after_opening_and_before_closing_bracket(self):
        function_arguments = arguments() \
            .add(spaces('    ')) \
            .add(unquoted_argument('NAME')) \
            .add(spaces(' '))
        expected_formatting = 'abc(NAME)'
        self.assertFormattingArguments(expected_formatting, function_arguments)

    def test_trimming_spaces_between_arguments(self):
        text = 'a text with \t tab    and multiple spaces'
        function_arguments = arguments() \
            .add(spaces('    ')) \
            .add(unquoted_argument('NAME')) \
            .add(spaces('    ')) \
            .add(quoted_argument(text)) \
            .add(spaces(' '))

        expected_formatting = f'abc(NAME \"{text}\")'
        self.assertFormattingArguments(expected_formatting, function_arguments)

    def test_indentation_of_arguments_in_newlines(self):
        function_arguments = arguments() \
            .add(newlines(4)) \
            .add(spaces('    ')) \
            .add(unquoted_argument('NAME')) \
            .add(newlines(4)) \
            .add(spaces('    ')) \
            .add(quoted_argument('XYZ')) \
            .add(spaces(' '))

        expected_formatting = f'abc(\n  NAME\n  \"XYZ\")'
        self.assertFormattingArguments(expected_formatting, function_arguments)
