###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from tests.unit.parser_composite_elements import arguments, newlines, spaces, unquoted_argument, file, \
    command_invocation
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandInvocationsWrapping(TestCMakeFormatter):
    def test_invocation_wrapping_for_short_function(self):
        self.settings['wrap_short_invocations_to_single_line'] = True
        args = arguments() \
            .add(newlines(4)) \
            .add(spaces('    ')) \
            .add(unquoted_argument('argument1')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('argument2')) \
            .add(newlines(4))
        root = file().add(command_invocation('function_call(', args))

        expected_formatting = """function_call(argument1 argument2)"""

        self.assertFormatting(expected_formatting, root)

    def test_invocation_wrapping_only_when_line_length_is_smaller_than_set_threshold(self):
        self.settings['wrap_short_invocations_to_single_line'] = True
        self.settings['line_length'] = 15

        args = arguments() \
            .add(newlines(1)) \
            .add(unquoted_argument('abc')) \
            .add(newlines(1)) \
            .add(unquoted_argument('def'))
        wrappable_invocation = command_invocation('wr(', args)
        not_wrappable_invocation = command_invocation('a_very_long_name_command(', args)
        root = file().add(wrappable_invocation) \
            .add(newlines(1)) \
            .add(not_wrappable_invocation)

        expected_formatting = """wr(abc def)
a_very_long_name_command(
  abc
  def)"""

        self.assertFormatting(expected_formatting, root)
