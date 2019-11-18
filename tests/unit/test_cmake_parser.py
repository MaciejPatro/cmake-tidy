import unittest

from cmake_tidy.parsing.cmake_parser import CMakeParser
from cmake_tidy.parsing.elements import PrimitiveElement
from tests.unit.parser_composite_elements import spaces_file_element, line_comment, newlines, unhandled_file_element, file


class TestCMakeParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = CMakeParser()

    def assertReprEqual(self, expected, received):
        self.assertEqual(str(expected), str(received))


class TestParseBasicElements(TestCMakeParser):
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
            .add(spaces_file_element(spacing)) \
            .add(unhandled_file_element(end))

        self.assertReprEqual(root, self.parser.parse(begin + spacing + end))
