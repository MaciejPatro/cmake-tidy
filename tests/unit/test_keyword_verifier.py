###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest

from cmake_tidy.utils.keyword_verifier import KeywordVerifier


class TestKeywordVerifier(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = {'keywords': ['TARGET', 'some'], 'unquoted_uppercase_as_keyword': False}

    def test_should_accept_keyword_when_on_the_list(self):
        verify = KeywordVerifier(self.settings)

        self.assertTrue(verify.is_keyword('TARGET'))
        self.assertTrue(verify.is_keyword('some'))
        self.assertFalse(verify.is_keyword('TARGET2'))
        self.assertFalse(verify.is_keyword('${TARGET}'))

    def test_no_keywords_should_only_return_false(self):
        verify = KeywordVerifier({})
        self.assertFalse(verify.is_keyword('TARGET'))

    def test_unquoted_arguments_with_uppercase_letters_only_are_keywords(self):
        self.settings['unquoted_uppercase_as_keyword'] = True
        verify = KeywordVerifier(self.settings)

        self.assertTrue(verify.is_keyword('TARGET'))
        self.assertTrue(verify.is_keyword('OTHER'))
        self.assertFalse(verify.is_keyword('WITH_SEPARATION'))
        self.assertFalse(verify.is_keyword('"$OTHER"'))
