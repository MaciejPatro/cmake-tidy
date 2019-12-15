from tests.unit.parser_composite_elements import spaces, file, command_invocation, unquoted_argument, \
    arguments
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandArguments(TestCMakeFormatter):
    def test_no_spaces_after_opening_and_before_closing_bracket(self):
        function_arguments = arguments() \
            .add(spaces('    ')) \
            .add(unquoted_argument('NAME')) \
            .add(spaces(' '))
        function_with_invocation_in_second_line = file().add(command_invocation('function(', function_arguments))
        expected_formatting = 'function(NAME)'
        self.assertFormatting(expected_formatting, function_with_invocation_in_second_line)
