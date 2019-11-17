import unittest

from cmake_tidy.parsing.cmake_parser import CMakeParser
from cmake_tidy.parsing.elements import PrimitiveElement
from tests.unit.parser_composite_elements import spaces, line_comment, newlines, bracket_argument, quoted_argument, \
    unquoted_argument, command_invocation, unhandled_file_element, file, arguments, unhandled


class TestCMakeParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = CMakeParser()

    def test_should_parse_correctly_empty_input(self):
        self.assertReprEqual(PrimitiveElement(), self.parser.parse(''))

    def test_should_parse_correctly_newlines(self):
        file_with_new_lines = file().add(newlines(2))
        self.assertReprEqual(file_with_new_lines, self.parser.parse('\n\n'))

    def test_should_parse_with_unhandled_data_still_collecting_output(self):
        root = file() \
            .add(newlines(1)) \
            .add(unhandled_file_element('aaa')) \
            .add(newlines(2))

        self.assertReprEqual(root, self.parser.parse('\naaa\n\n'))

    def test_should_handle_line_comments(self):
        comment = '# comment here'
        root = file().add(line_comment(comment, 2))

        self.assertReprEqual(root, self.parser.parse(comment + '\n\n'))

    def test_should_parse_line_comments_and_unhandled_data_together(self):
        comment = '# cdaew9u32#$#@%#232cd a2o#@$@!'
        root = file() \
            .add(line_comment(comment, 1)) \
            .add(unhandled_file_element('xc_43'))

        self.assertReprEqual(root, self.parser.parse(comment + '\nxc_43'))

    def test_should_parse_spacings_within_text(self):
        begin = 'abc'
        spacing = '  \t'
        end = '_\"DWa'
        root = file().add(unhandled_file_element(begin)) \
            .add(spaces(spacing)) \
            .add(unhandled_file_element(end))

        self.assertReprEqual(root, self.parser.parse(begin + spacing + end))

    def test_parsing_command_invocation_without_arguments(self):
        start_invocation = 'include('
        root = file().add(command_invocation(start_invocation, []))

        self.assertReprEqual(root, self.parser.parse(start_invocation + ')'))

    def test_parsing_command_invocation_with_arguments_and_spaces(self):
        start_invocation = 'include \t('
        func_arguments = 'CTest, 123'

        expected_arguments = arguments().add(unhandled(func_arguments))
        root = file().add(command_invocation(start_invocation, expected_arguments))

        self.assertReprEqual(root, self.parser.parse(f'{start_invocation}{func_arguments})'))

    def test_parsing_command_invocation_with_bracket_argument(self):
        start_invocation = 'function_name('
        bracket_start = '[==['
        bracket_end = ']==]'
        bracket_argument_data = 'this is bracket_dwad832423#$@#$ content]===] still there'

        root = file().add(command_invocation(start_invocation,
                                             arguments().add(bracket_argument(2, bracket_argument_data))))

        self.assertReprEqual(root, self.parser.parse(
            f'{start_invocation}{bracket_start}{bracket_argument_data}{bracket_end})'))

    def test_parsing_command_invocation_with_quoted_argument_with_escaped_quote_inside(self):
        start_invocation = 'name('
        argument_content = 'simple\n\\\" text'
        root = file().add(
            command_invocation(start_invocation,
                               arguments().add(quoted_argument(argument_content)))
        )

        self.assertReprEqual(root, self.parser.parse(
            f'{start_invocation}"{argument_content}")'))

    def test_parsing_command_invocation_with_basic_unquoted_argument(self):
        start_invocation = 'name('
        argument_content = 'simple_argument'
        root = file().add(
            command_invocation(start_invocation,
                               arguments().add(unquoted_argument(argument_content)))
        )

        self.assertReprEqual(root, self.parser.parse(
            f'{start_invocation}{argument_content})'))

    def assertReprEqual(self, expected, received):
        self.assertEqual(str(expected), str(received))
