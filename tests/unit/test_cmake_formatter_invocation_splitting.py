###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from tests.unit.parser_composite_elements import arguments, spaces, unquoted_argument, file, command_invocation, \
    line_ending, newlines, quoted_argument
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

    def test_invocation_when_keyword_and_single_values_keep_in_single_line(self):
        self.settings['keyword_and_single_value_in_one_line'] = True
        args = arguments().add(newlines(1)) \
            .add(unquoted_argument('FILES')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('file.cpp')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('file.hpp')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('DESTINATION')) \
            .add(spaces('    ')) \
            .add(quoted_argument('include/folder')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('NAMESPACE')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('unofficial::graphicsmagick::')) \
            .add(newlines(1))

        root = file().add(command_invocation('install(', args))

        expected_formatting = """install(
  FILES
    file.cpp
    file.hpp
  DESTINATION "include/folder"
  NAMESPACE unofficial::graphicsmagick::
)"""
        self.assertFormatting(expected_formatting, root)

    def test_invocation_when_keyword_and_single_values_keep_in_single_line_comments_case_at_the_end(self):
        self.settings['keyword_and_single_value_in_one_line'] = True
        args = arguments().add(newlines(1)) \
            .add(unquoted_argument('FILES')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('file.cpp')) \
            .add(spaces('    ')) \
            .add(line_ending('# comment', 1))

        root = file().add(command_invocation('install(', args))

        expected_formatting = """install(
  FILES file.cpp # comment
)"""
        self.assertFormatting(expected_formatting, root)

    def test_invocation_when_keyword_and_single_values_keep_in_single_line_comments_case_in_the_middle(self):
        self.settings['keyword_and_single_value_in_one_line'] = True
        args = arguments().add(newlines(1)) \
            .add(unquoted_argument('DESTINATION')) \
            .add(spaces('    ')) \
            .add(quoted_argument('include/folder')) \
            .add(spaces('    ')) \
            .add(line_ending('# comment', 1)) \
            .add(unquoted_argument('NAMESPACE')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('unofficial::graphicsmagick::')) \
            .add(newlines(1))

        root = file().add(command_invocation('install(', args))

        expected_formatting = """install(
  DESTINATION
    "include/folder" # comment
  NAMESPACE unofficial::graphicsmagick::
)"""
        self.assertFormatting(expected_formatting, root)

    def test_invocation_when_keyword_is_first_argument_move_to_newline(self):
        self.settings['keyword_and_single_value_in_one_line'] = True
        self.settings['line_length'] = 5
        args = arguments() \
            .add(unquoted_argument('FILES')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('file.cpp')) \
            .add(newlines(1))

        root = file().add(command_invocation('install(', args))
        self.assertFormatting('install(\n  FILES file.cpp\n)', root)

    def test_invocation_when_double_keyword_occurs_should_keep_it_in_one_line(self):
        self.settings['keyword_and_single_value_in_one_line'] = True
        self.settings['line_length'] = 5
        args = arguments().add(newlines(1)) \
            .add(unquoted_argument('ARCHIVE')) \
            .add(newlines(1)) \
            .add(unquoted_argument('DESTINATION')) \
            .add(spaces('    ')) \
            .add(quoted_argument('include/folder')) \
            .add(newlines(1))

        root = file().add(command_invocation('install(', args))

        expected_formatting = """install(
  ARCHIVE DESTINATION "include/folder"
)"""
        self.assertFormatting(expected_formatting, root)
