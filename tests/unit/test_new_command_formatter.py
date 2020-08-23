###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest
from typing import Iterable

from cmake_tidy.formatting.utils.invocation.new_command_formatter import NewCommandFormatter


def make_invocation(name: str, arguments: Iterable[str]) -> dict:
    return {'function_name': name, 'arguments': arguments, 'closing': ')'}


class TestNewCommandFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.state = dict()
        self.settings = dict()
        self.formatter = NewCommandFormatter(self.state, self.settings)

    def test_format_empty_invocation(self):
        self.assertEqual('set()', self.formatter.format(make_invocation('set(', [])))

    def test_invocation_with_single_argument(self):
        self.assertEqual('set(argument)', self.formatter.format(make_invocation('set(', ['argument'])))
