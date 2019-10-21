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
            .add(unhandled('aaa')) \
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
            .add(unhandled('xc_43'))

        self.assertReprEqual(root, self.parser.parse(comment + '\nxc_43'))

    def test_should_parse_spacings_within_text(self):
        begin = 'abc'
        spacing = '  \t'
        end = '_\"DWa'
        root = file().add(unhandled(begin)) \
            .add(spaces(spacing)) \
            .add(unhandled(end))

        self.assertReprEqual(root, self.parser.parse(begin + spacing + end))

    def test_parsing_command_invocation_without_arguments(self):
        start_invocation = 'include('
        root = file().add(
            command_invocation([PrimitiveElement('start_cmd_invoke', start_invocation),
                                PrimitiveElement('arguments', ''),
                                PrimitiveElement('end_cmd_invoke', ')')]))

        self.assertReprEqual(root, self.parser.parse(start_invocation + ')'))

    def test_parsing_command_invocation_with_arguments_and_spaces(self):
        start_invocation = 'include \t('
        arguments = 'CTest, 123'
        root = file().add(
            command_invocation([PrimitiveElement('start_cmd_invoke', start_invocation),
                                PrimitiveElement('arguments', arguments),
                                PrimitiveElement('end_cmd_invoke', ')')]))

        self.assertReprEqual(root, self.parser.parse(start_invocation + arguments + ')'))

    def assertReprEqual(self, expected, received):
        self.assertEqual(str(expected), str(received))


def file() -> Element:
    return ComplexElement('file')


def file_element() -> Element:
    return ComplexElement('file_element')


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


def unhandled(data: str) -> Element:
    return ComplexElement('file_element').add(PrimitiveElement('unhandled', data))


def command_invocation(elements: list):
    cmd_invocation = ComplexElement('command_invocation')
    for element in elements:
        cmd_invocation.add(element)
    return ComplexElement('file_element').add(cmd_invocation)
