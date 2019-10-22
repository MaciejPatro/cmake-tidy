import unittest

from cmake_tidy.parsing.cmake_parser import CMakeParser
from cmake_tidy.parsing.elements import PrimitiveElement, Element, ComplexElement


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
        bracket_argument = 'this is bracket_dwad832423#$@#$ content]===] still there'

        expected_arguments = arguments() \
            .add(PrimitiveElement('start_bracket_argument', 2)) \
            .add(PrimitiveElement('bracket_argument_content', bracket_argument)) \
            .add(PrimitiveElement('end_bracket_argument', 2))
        root = file().add(command_invocation(start_invocation, expected_arguments))

        self.assertReprEqual(root, self.parser.parse(f'{start_invocation}[==[{bracket_argument}]==])'))

    def assertReprEqual(self, expected, received):
        self.assertEqual(str(expected), str(received))


def spaces(data: str) -> Element:
    return ComplexElement('file_element').add(PrimitiveElement('spaces', data))


def line_comment(comment: str, newlines_number: int) -> Element:
    return ComplexElement('file_element') \
        .add(ComplexElement('line_ending')
             .add(PrimitiveElement('line_comment', comment))
             .add(PrimitiveElement('newlines', newlines_number)))


def newlines(number: int) -> Element:
    return ComplexElement('file_element').add(
        ComplexElement('line_ending').add(PrimitiveElement('newlines', number)))


def command_invocation(func_name: str, args=None):
    cmd_invocation = ComplexElement('command_invocation') \
        .add(start_cmd(func_name)) \
        .add(args) \
        .add(end_cmd())
    return ComplexElement('file_element').add(cmd_invocation)


def unhandled_file_element(data: str) -> Element:
    return ComplexElement('file_element').add(unhandled(data))


def file() -> Element:
    return ComplexElement('file')


def file_element() -> Element:
    return ComplexElement('file_element')


def arguments() -> Element:
    return ComplexElement('arguments')


def start_cmd(name: str) -> PrimitiveElement:
    return PrimitiveElement('start_cmd_invoke', name)


def end_cmd() -> PrimitiveElement:
    return PrimitiveElement('end_cmd_invoke', ')')


def unhandled(data: str) -> PrimitiveElement:
    return PrimitiveElement('unhandled', data)
