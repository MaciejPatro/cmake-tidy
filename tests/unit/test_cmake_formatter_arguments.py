###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################
from tests.unit.parser_composite_elements import spaces, file, command_invocation, unquoted_argument, \
    arguments, quoted_argument, newlines, bracket_argument, line_ending
from tests.unit.test_cmake_formatter import TestCMakeFormatter


class TestCMakeFormatterCommandArguments(TestCMakeFormatter):
    def assertFormattingArguments(self, expected_formatting, function_arguments):
        self.assertFormatting(expected_formatting, file().add(command_invocation('abc(', function_arguments)))

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
            .add(unquoted_argument('NAME')) \
            .add(newlines(4)) \
            .add(spaces('    ')) \
            .add(quoted_argument('XYZ')) \
            .add(spaces(' '))

        expected_formatting = f'abc(\n  NAME\n  \"XYZ\")'
        self.assertFormattingArguments(expected_formatting, function_arguments)

    def test_indentation_should_not_apply_to_content_of_bracket_argument_endif_should_be_indented(self):
        function_arguments = arguments() \
            .add(newlines(4)) \
            .add(spaces('    ')) \
            .add(bracket_argument(2, 'text\n  endif(\nother'))

        expected_formatting = f'abc(\n  [==[text\n  endif(\nother]==])'
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
        self.settings['keywords'] = ['INTERFACE_LINK_DEPENDS', 'JOB_POOL_COMPILE']
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
        self.settings['keywords'] = ['TARGET']

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
        self.settings['line_length'] = 10
        self.settings['keywords'] = ['TARGET', 'FOO']

        args = arguments().add(unquoted_argument('abcd')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('PROPERTIES')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('FOO')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('TARGET')) \
            .add(spaces('    ')) \
            .add(unquoted_argument('def'))

        root = file().add(command_invocation('some_name(', args))

        expected_formatting = """some_name(abcd
  PROPERTIES
    FOO def
    TARGET def)"""
        self.assertFormatting(expected_formatting, root)
