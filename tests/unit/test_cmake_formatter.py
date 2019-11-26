import unittest

from cmake_tidy.formatting import CMakeFormatter
from cmake_tidy.parsing.elements import PrimitiveElement
from tests.unit.parser_composite_elements import spaces, newlines


class TestCMakeFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.__settings = {'succeeding_newlines': 1, 'tab_size': 2}

    def test_return_single_newline(self):
        f = CMakeFormatter(self.__settings)
        self.assertEqual('\n', f.format(newlines(3)))

    def test_return_3_newlines_although_settings_allow_more(self):
        self.__settings['succeeding_newlines'] = 5
        f = CMakeFormatter(self.__settings)
        self.assertEqual('\n\n\n', f.format(newlines(3)))

    def test_replace_tab_with_space_one_to_two(self):
        f = CMakeFormatter(self.__settings)
        self.assertEqual(' ' * 4, f.format(spaces('\t\t')))

    def test_replace_tabs_with_multiple_spaces(self):
        self.__settings['tab_size'] = 4
        f = CMakeFormatter(self.__settings)

        self.assertEqual(' ' * 10, f.format(spaces(' \t \t')))
