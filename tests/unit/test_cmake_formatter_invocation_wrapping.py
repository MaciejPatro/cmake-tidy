from tests.unit.parser_composite_elements import arguments, newlines, spaces, unquoted_argument, file, \
    command_invocation
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandInvocationsWrapping(TestCMakeFormatter):
    def test_invocation_wrapping_for_short_function(self):
        self.settings['wrap_short_invocations_to_single_line'] = True
        args = arguments() \
                .add(newlines(4)) \
                .add(spaces('    ')) \
                .add(unquoted_argument('argument'))
        root = file().add(command_invocation('function_call(', args))

        expected_formatting = """function_call(argument)"""

        self.assertFormatting(expected_formatting, root)

    def test_invocation_wrapping_only_when_line_length_is_smaller_than_set_threshold(self):
        self.settings['wrap_short_invocations_to_single_line'] = True
        self.settings['line_length'] = 15

        args = arguments().add(newlines(1)).add(unquoted_argument('abc'))
        wrappable_invocation = command_invocation('wrapped(', args)
        not_wrappable_invocation = command_invocation('a_very_long_name_command(', args)
        root = file().add(wrappable_invocation) \
            .add(newlines(1)) \
            .add(not_wrappable_invocation)

        expected_formatting = """wrapped(abc)
a_very_long_name_command(
  abc)"""

        self.assertFormatting(expected_formatting, root)
