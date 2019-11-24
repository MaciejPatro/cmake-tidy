import unittest

from cmake_tidy.formatting.utils import FormatNewlines, FormatSpaces, FormatLineEnding


class TestFormatNewlines(unittest.TestCase):
    def test_return_single_newline(self):
        format_newlines = FormatNewlines({'succeeding_newlines': 1})
        self.assertEqual('\n', format_newlines(3))

    def test_return_2_newlines_altough_settings_allow_more(self):
        format_newlines = FormatNewlines({'succeeding_newlines': 5})
        self.assertEqual('\n\n', format_newlines(2))


class TestFormatSpaces(unittest.TestCase):
    def test_replace_tab_with_space_one_to_one(self):
        format_spaces = FormatSpaces({'tab_size': 1})
        self.assertEqual(' ' * 4, format_spaces(' \t \t'))

    def test_replace_tabs_with_multiple_spaces(self):
        format_spaces = FormatSpaces({'tab_size': 4})
        self.assertEqual(' ' * 10, format_spaces(' \t \t'))


class TestFormatLineEnding(unittest.TestCase):
    def test_line_ending_should_merge_comments_and_newlines(self):
        comment = '# comment'
        newline = '\n'

        format_line_ending = FormatLineEnding()

        self.assertEqual(comment + newline, format_line_ending([comment, newline]))
