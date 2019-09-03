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
        root = file().add(newlines(1))\
            .add(unhandled('aaa'))\
            .add(newlines(2))

        self.assertReprEqual(root, self.parser.parse('\naaa\n\n'))

    def assertReprEqual(self, expected, received):
        self.assertEqual(str(expected), str(received))


def file() -> Element:
    return ComplexElement('file')


def newlines(number: int) -> PrimitiveElement:
    return PrimitiveElement('newlines', number)


def unhandled(data: str) -> PrimitiveElement:
    return PrimitiveElement('unhandled', data)
