###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from tests.unit.parser_composite_elements import arguments, unquoted_argument, spaces, \
    quoted_argument, newlines, parentheses
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterConditionalWithParentheses(TestCMakeFormatter):
    def setUp(self) -> None:
        super().setUp()
        self.settings['condition_splitting_move_and_or_to_newline'] = True

    def test_split_with_parentheses(self):
        condition = parentheses().add(arguments()
                                      .add(unquoted_argument('${CMAKE_CXX_COMPILER_ID}')).add(spaces(' '))
                                      .add(unquoted_argument('STREQUAL')).add(spaces(' '))
                                      .add(quoted_argument('GNU')).add(newlines(5))
                                      .add(unquoted_argument('AND')).add(newlines(1))
                                      .add(unquoted_argument('${CMAKE_CXX_COMPILER_VERSION}')).add(spaces(' '))
                                      .add(unquoted_argument('VERSION_LESS')).add(spaces(' '))
                                      .add(quoted_argument('9')))

        expected_formatting = """if((${CMAKE_CXX_COMPILER_ID} STREQUAL "GNU"
      AND ${CMAKE_CXX_COMPILER_VERSION} VERSION_LESS "9"))"""

        self.assertConditionFormatting(expected_formatting, arguments().add(condition))
