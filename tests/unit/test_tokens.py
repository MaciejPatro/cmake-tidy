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
