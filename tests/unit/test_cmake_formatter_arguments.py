###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from tests.unit.parser_composite_elements import spaces, file, command_invocation, unquoted_argument, \
    arguments, quoted_argument, newlines, bracket_argument, line_ending
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandArguments(TestCMakeFormatter):
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
            .add(unquoted_argument('NAMING')) \
            .add(newlines(4)) \
            .add(spaces('    ')) \
            .add(quoted_argument('XYZ')) \
            .add(spaces(' '))

        expected_formatting = f'abc(\n  NAMING\n  \"XYZ\")'
        self.assertFormattingArguments(expected_formatting, function_arguments)

    def test_indentation_should_not_apply_to_content_of_bracket_argument_endif_should_be_indented(self):
        function_arguments = arguments() \
            .add(newlines(4)) \
            .add(spaces('    ')) \
            .add(bracket_argument(2, 'text\n  endif(\nother'))

        expected_formatting = f'abc(\n[==[text\n  endif(\nother]==])'
        self.assertFormattingArguments(expected_formatting, function_arguments)

    def test_ident_target_keyword_in_command(self):
        function_arguments = arguments() \
            .add(newlines(4)) \
            .add(unquoted_argument('TARGET')) \
            .add(newlines(4)) \
            .add(unquoted_argument('text')) \
            .add(newlines(4)) \
            .add(unquoted_argument('TARGET')) \
            .add(newlines(4)) \
            .add(bracket_argument(2, 'text')) \
            .add(newlines(4))

        expected_formatting = 'abc(\n  TARGET\n    text\n  TARGET\n    [==[text]==]\n)'
        self.assertFormattingArguments(expected_formatting, function_arguments)

    def test_ident_set_target_properties_example(self):
        function_arguments = arguments() \
            .add(unquoted_argument('target_name')) \
            .add(newlines(4)) \
            .add(unquoted_argument('PROPERTIES')) \
            .add(newlines(4)) \
            .add(unquoted_argument('INTERFACE_LINK_DEPENDS')) \
            .add(newlines(4)) \
            .add(unquoted_argument('${VALUE}')) \
            .add(newlines(4)) \
            .add(unquoted_argument('JOB_POOL_COMPILE')) \
            .add(newlines(4)) \
            .add(unquoted_argument('${VALUE2}')) \
            .add(newlines(4))

        expected_formatting = """abc(target_name
  PROPERTIES
    INTERFACE_LINK_DEPENDS
      ${VALUE}
    JOB_POOL_COMPILE
      ${VALUE2}
)"""
        self.assertFormattingArguments(expected_formatting, function_arguments)

    def test_splitting_long_line_with_multiple_arguments_and_properties(self):
        self.settings['line_length'] = 30
        self.settings['closing_parentheses_in_newline_when_split'] = True

        args = arguments().add(unquoted_argument('abcd')) \
            .add(spaces('    ')) \
            .add(line_ending('# comment', 1)) \
            .add(unquoted_argument('some_target')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('PROPERTIES')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def'))

        root = file().add(command_invocation('some_name(', args))

        expected_formatting = """some_name(abcd # comment
  some_target
  PROPERTIES
    TARGET
      def
    TARGET
      def
)"""
        self.assertFormatting(expected_formatting, root)

    def test_splitting_while_properties_keep_same_line(self):
        self.settings['keep_property_and_value_in_one_line'] = True
        self.settings['line_length'] = 10
        self.settings['keywords'] = ['BAR', 'TARGET', 'FOO']

        args = arguments().add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('abcd')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('PROPERTIES')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('FOO')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('BAR')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def2'))

        root = file().add(command_invocation('set_property(', args))

        expected_formatting = """set_property(
  TARGET abcd
  PROPERTIES
    FOO def
    BAR def2)"""
        self.assertFormatting(expected_formatting, root)

    def test_splitting_custom_target_command(self):
        self.settings['line_length'] = 10
        self.settings['keep_command_in_single_line'] = True

        args = arguments().add(unquoted_argument('${target}-resources')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('COMMAND')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('${CMAKE_COMMAND}')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('-E')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('echo')) \
            .add(spaces('    ')) \
            .add(quoted_argument('Copy resource files for ${target}'))

        root = file().add(command_invocation('add_custom_target(', args))

        expected_formatting = """add_custom_target(${target}-resources
  COMMAND
    ${CMAKE_COMMAND} -E echo "Copy resource files for ${target}")"""

        self.assertFormatting(expected_formatting, root)

    def test_empty_spaces_at_end_of_line(self):
        self.settings['line_length'] = 10
        self.settings['keyword_and_single_value_in_one_line'] = True

        args = arguments().add(unquoted_argument('abc')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(newlines(1)) \
            .add(unquoted_argument('${PROJECT_NAME}')) \
            .add(newlines(1))

        root = file().add(command_invocation('add_custom_target(', args))
        self.assertFormatting('add_custom_target(abc\n  TARGET ${PROJECT_NAME}\n)', root)
