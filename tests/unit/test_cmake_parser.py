import unittest

from cmake_tidy.parsing.cmake_parser import CMakeParser


class TestCMakeParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = CMakeParser()

    def test_should_parse_correctly_empty_input(self):
        self.assertRepresentationEqual('', self.parser.parse(''))

    def assertRepresentationEqual(self, expected, obj):
        self.assertEqual(expected, str(obj))
