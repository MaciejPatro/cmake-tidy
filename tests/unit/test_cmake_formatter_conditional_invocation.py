###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################
from unittest import skip

from cmake_tidy.lexical_data.elements import Element
from tests.unit.parser_composite_elements import arguments, unquoted_argument, spaces, file, command_invocation, \
    quoted_argument, line_ending, newlines
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterConditionalInvocation(TestCMakeFormatter):
    def assertConditionFormatting(self, expected: str, args: Element):
        root = file().add(command_invocation('if(', args))
        self.assertFormatting(expected, root)

    def test_already_aligned_invocation(self):
        args = arguments() \
            .add(unquoted_argument('abc')).add(spaces(' ')) \
            .add(unquoted_argument('OR')).add(spaces(' ')) \
            .add(unquoted_argument('def'))

        self.assertConditionFormatting('if(abc OR def)', args)

    def test_splitting_only_after_logical_operations(self):
        self.settings['line_length'] = 10

        args = arguments() \
            .add(unquoted_argument('CMAKE_C_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU')).add(spaces(' ')) \
            .add(unquoted_argument('AND')).add(spaces(' ')) \
            .add(unquoted_argument('CMAKE_CXX_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU'))

        expected_formatting = """if(CMAKE_C_COMPILER_ID STREQUAL "GNU" AND
    CMAKE_CXX_COMPILER_ID STREQUAL "GNU")"""
        self.assertConditionFormatting(expected_formatting, args)

    def test_already_split_condition_should_have_correct_indent(self):
        args = arguments() \
            .add(unquoted_argument('CMAKE_C_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU')).add(spaces(' ')) \
            .add(unquoted_argument('AND')).add(spaces(' ')) \
            .add(newlines(1)) \
            .add(unquoted_argument('CMAKE_CXX_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU'))

        expected_formatting = """if(CMAKE_C_COMPILER_ID STREQUAL "GNU" AND
    CMAKE_CXX_COMPILER_ID STREQUAL "GNU")"""
        self.assertConditionFormatting(expected_formatting, args)

    @skip('First new test is needed')
    def test_splitting_only_after_logical_operations_comments_excluded(self):
        self.settings['line_length'] = 10

        args = arguments() \
            .add(unquoted_argument('CMAKE_C_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU')).add(spaces(' ')) \
            .add(unquoted_argument('AND')).add(spaces(' ')) \
            .add(line_ending('# a comment', 1)) \
            .add(unquoted_argument('CMAKE_CXX_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU'))

        expected_formatting = """if(CMAKE_C_COMPILER_ID STREQUAL "GNU" AND # a comment
    CMAKE_CXX_COMPILER_ID STREQUAL "GNU")"""
        self.assertConditionFormatting(expected_formatting, args)
