###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest

from cmake_tidy.formatting.utils.tokens import Tokens


class TestTokens(unittest.TestCase):
    def test_reindent_token_generation_and_matching(self):
        self.assertRegex(Tokens.reindent(1), Tokens.get_reindent_regex())
        self.assertRegex(Tokens.reindent(9), Tokens.get_reindent_regex())

    def test_matching_line_comment_tokens(self):
        self.assertTrue(Tokens.is_line_comment('# comment'))
        self.assertTrue(Tokens.is_line_comment('#comment'))
        self.assertTrue(Tokens.is_line_comment(Tokens.reindent(1) + '#comment'))
        self.assertTrue(Tokens.is_line_comment('\t # something'))
        self.assertTrue(Tokens.is_line_comment('\t #'))
        self.assertFalse(Tokens.is_line_comment('_# not a comment'))
        self.assertFalse(Tokens.is_line_comment('comment'))

    def test_matching_spacing_tokens(self):
        self.assertFalse(Tokens.is_line_comment(''))
        self.assertTrue(Tokens.is_spacing_token(' '))
        self.assertTrue(Tokens.is_spacing_token('\t '))
        self.assertTrue(Tokens.is_spacing_token('\t \n'))
        self.assertTrue(Tokens.is_spacing_token(f'\t {Tokens.remove_spaces()}\n'))
        self.assertFalse(Tokens.is_spacing_token('\t d'))
        self.assertFalse(Tokens.is_spacing_token(f'\t {Tokens.reindent(1)}'))
