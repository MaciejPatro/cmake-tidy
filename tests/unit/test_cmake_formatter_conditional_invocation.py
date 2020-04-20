###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.lexical_data.elements import Element
from tests.unit.parser_composite_elements import arguments, unquoted_argument, spaces, file, command_invocation, \
    quoted_argument
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
        self.settings['line_length'] = 100

        args = arguments() \
            .add(unquoted_argument('CMAKE_C_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU')).add(spaces(' ')) \
            .add(unquoted_argument('AND')).add(spaces(' ')) \
            .add(unquoted_argument('CMAKE_CXX_COMPILER_ID')).add(spaces(' ')) \
            .add(unquoted_argument('STREQUAL')).add(spaces(' ')) \
            .add(quoted_argument('GNU'))

        expected_formatting = """if(CMAKE_C_COMPILER_ID STREQUAL "GNU" AND 
    CMAKE_CXX_COMPILER_ID STREQUAL "GNU"
)"""
        self.assertConditionFormatting(expected_formatting, args)
