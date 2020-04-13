###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from tests.unit.parser_composite_elements import arguments, spaces, unquoted_argument, file, command_invocation, \
    line_ending, newlines
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandInvocationSplitting(TestCMakeFormatter):
    def test_invocation_splitting_when_line_length_exceeded(self):
        self.settings['line_length'] = 15
        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def'))
        root = file().add(command_invocation('a_very_long_name(', args))

        expected_formatting = """a_very_long_name(abc
  def)"""
        self.assertFormatting(expected_formatting, root)

    def test_invocation_splitting_with_closing_parentheses_in_newline(self):
        self.settings['line_length'] = 15
        self.settings['closing_parentheses_in_newline_when_split'] = True
        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def'))
        root = file().add(command_invocation('a_very_long_name(', args))

        expected_formatting = """a_very_long_name(abc
  def
)"""
        self.assertFormatting(expected_formatting, root)

    def test_invocation_splitting_with_closing_parentheses_in_newline_and_keyword(self):
        self.settings['line_length'] = 15
        self.settings['closing_parentheses_in_newline_when_split'] = True
        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def'))
        root = file().add(command_invocation('a_very_long_name(', args))

        expected_formatting = """a_very_long_name(abc
  TARGET
    def
)"""
        self.assertFormatting(expected_formatting, root)

    def test_invocation_splitting_with_closing_parentheses_in_newline_and_newline_already_there(self):
        self.settings['line_length'] = 5
        self.settings['closing_parentheses_in_newline_when_split'] = True
        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(newlines(1))

        root = file().add(command_invocation('a_very_long_name(', args))

        expected_formatting = """a_very_long_name(abc
  TARGET
)"""
        self.assertFormatting(expected_formatting, root)

    def test_invocation_splitting_with_keywords_inside(self):
        self.settings['line_length'] = 5
        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def'))

        root = file().add(command_invocation('function(', args))

        expected_formatting = """function(abc
  TARGET
    def
  TARGET
    def)"""

        self.assertFormatting(expected_formatting, root)

    def test_invocation_splitting_with_line_comments(self):
        self.settings['line_length'] = 5
        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(line_ending('# comment', 1)) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def'))

        root = file().add(command_invocation('function(', args))

        expected_formatting = """function(abc # comment
  TARGET
    def)"""

        self.assertFormatting(expected_formatting, root)
