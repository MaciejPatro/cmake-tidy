###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re
import unittest
from typing import Iterable

from cmake_tidy.formatting.utils.invocation.new_command_formatter import NewCommandFormatter
from cmake_tidy.formatting.utils.tokens import Tokens


class TestNewCommandFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.state = {'indent': 0}
        self.settings = {'line_length': 80, 'tabs_as_spaces': False, 'succeeding_newlines': 2,
                         'closing_parentheses_in_newline_when_split': False,
                         'wrap_short_invocations_to_single_line': False}
        self.formatter = NewCommandFormatter(self.state, self.settings)

    def test_format_empty_invocation(self):
        self.assertEqual('set()', self.__get_formatted('set(', []))

    def test_invocation_with_single_argument(self):
        self.assertEqual('set(argument)', self.__get_formatted('set(', ['argument']))

    def test_invocation_two_arguments_fitting(self):
        self.assertEqual('set(argument next)', self.__get_formatted('set(', ['argument', ' ', 'next']))

    def test_wrapping_invocation_when_it_fits(self):
        self.settings['wrap_short_invocations_to_single_line'] = True
        self.assertEqual('set(argument next)', self.__get_formatted('set(', ['argument', '\t\n', 'next']))

    @staticmethod
    def __make_invocation(name: str, arguments: Iterable[str]) -> dict:
        return {'function_name': name, 'arguments': arguments, 'closing': ')'}

    def __get_formatted(self, name: str, arguments: Iterable[str]) -> str:
        raw = self.formatter.format(self.__make_invocation(name, arguments))
        return re.sub(Tokens.remove_spaces(), '', raw)
