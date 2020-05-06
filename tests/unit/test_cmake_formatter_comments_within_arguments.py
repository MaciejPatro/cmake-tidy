###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from unittest import skip

from tests.unit.parser_composite_elements import spaces, file, command_invocation, unquoted_argument, \
    arguments, newlines, line_ending
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandArgumentsWithComments(TestCMakeFormatter):
    def test_multiple_line_comments_before_value(self):
        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(newlines(1)) \
            .add(line_ending('# first line', 1)) \
            .add(line_ending('# second line', 1)) \
            .add(unquoted_argument('${PROJECT_NAME}')) \
            .add(newlines(1))

        root = file().add(command_invocation('add_custom_target(', args))

        expected_formatting = """add_custom_target(abc
  TARGET
    # first line
    # second line
    ${PROJECT_NAME}
)"""
        self.assertFormatting(expected_formatting, root)

    @skip
    def test_multiple_line_comments_before_keyword(self):
        args = arguments().add(unquoted_argument('abc')) \
            .add(newlines(1)) \
            .add(unquoted_argument('ALL')) \
            .add(newlines(1)) \
            .add(line_ending('# first line', 1)) \
            .add(line_ending('# second line', 1)) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('  ')) \
            .add(unquoted_argument('${PROJECT_NAME}')) \
            .add(newlines(1))

        root = file().add(command_invocation('add_custom_target(', args))

        expected_formatting = """add_custom_target(abc
  ALL
  # first line
  # second line
  TARGET
    ${PROJECT_NAME}
)"""
        self.assertFormatting(expected_formatting, root)
