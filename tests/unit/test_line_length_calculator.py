###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest
from unittest import mock
from unittest.mock import MagicMock

from cmake_tidy.formatting.utils.line_length_calculator import LineLengthCalculator
from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.lexical_data import KeywordVerifier


class TestLineLengthCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = LineLengthCalculator({'tab_size': 4})

    def test_calculate_length_of_simple_strings(self):
        self.assertEqual(0, self.calculator.calculate(''))
        self.assertEqual(88, self.calculator.calculate(' ' * 88))
        self.assertEqual(16, self.calculator.calculate('some(invocation)'))

    def test_calculate_size_of_tabs(self):
        self.assertEqual(4, LineLengthCalculator({'tab_size': 4}).calculate('\t'))
        self.assertEqual(16, LineLengthCalculator({'tab_size': 8}).calculate('\t\t'))

    def test_ignore_reindent_tokens(self):
        self.assertEqual(0, self.calculator.calculate(Tokens.reindent(3)))
        self.assertEqual(14, self.calculator.calculate(f'\tsome{Tokens.reindent(99)}\tso'))

    def test_ignore_remove_spaces_tokens(self):
        self.assertEqual(0, self.calculator.calculate(Tokens.remove_spaces()))
        self.assertEqual(4, self.calculator.calculate(f'piwo{Tokens.remove_spaces()}'))
