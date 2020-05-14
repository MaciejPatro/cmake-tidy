###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest

from cmake_tidy.parsing.cmake_parser import CMakeParser
from cmake_tidy.lexical_data.elements import PrimitiveElement
from tests.unit.parser_composite_elements import file, line_ending, spaces, unhandled, newlines


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
            .add(unhandled('aaa')) \
            .add(newlines(2))

        self.assertReprEqual(root, self.parser.parse('\naaa\n\n'))

    def test_should_handle_line_comments(self):
        comment = '# comment here'
        root = file().add(line_ending(comment, 2))

        self.assertReprEqual(root, self.parser.parse(comment + '\n\n'))

    def test_should_handle_empty_comment(self):
        comment = '#'
        root = file().add(line_ending(comment, 2))

        self.assertReprEqual(root, self.parser.parse(comment + '\n\n'))

    def test_should_parse_line_comments_and_unhandled_data_together(self):
        comment = '# cdaew9u32#$#@%#232cd a2o#@$@!'
        root = file() \
            .add(line_ending(comment, 1)) \
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
