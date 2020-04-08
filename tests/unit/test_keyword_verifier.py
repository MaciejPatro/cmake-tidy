###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest
from unittest import mock
from unittest.mock import MagicMock

from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.lexical_data import KeywordVerifier


class TestKeywordVerifier(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = {'keywords': ['TARGET', 'some'], 'unquoted_uppercase_as_keyword': False}
        self.verify = KeywordVerifier(self.settings)

    def test_should_accept_keyword_when_on_the_list(self):
        self.assertTrue(self.verify.is_keyword('TARGET'))
        self.assertTrue(self.verify.is_keyword('some'))
        self.assertFalse(self.verify.is_keyword('TARGET2'))
        self.assertFalse(self.verify.is_keyword('${TARGET}'))

    def test_no_keywords_should_only_return_false(self):
        self.verify = KeywordVerifier({})
        self.assertFalse(self.verify.is_keyword('TARGET'))

    def test_unquoted_arguments_with_uppercase_letters_only_are_keywords(self):
        self.settings['unquoted_uppercase_as_keyword'] = True
        self.verify = KeywordVerifier(self.settings)

        self.assertTrue(self.verify.is_keyword('TARGET'))
        self.assertTrue(self.verify.is_keyword('OTHER'))
        self.assertTrue(self.verify.is_keyword(Tokens.reindent(1) + 'OTHER'))
        self.assertFalse(self.verify.is_keyword('WITH_SEPARATION'))
        self.assertFalse(self.verify.is_keyword('"$OTHER"'))

    @mock.patch('builtins.open')
    def test_ensure_properties_read_only_once(self, mock_open: MagicMock):
        self.verify = KeywordVerifier(self.settings)
        self.assertFalse(mock_open.called)

    def test_whether_token_is_first_class_keyword(self):
        self.assertTrue(self.verify.is_first_class_keyword('PROPERTY'))
        self.assertTrue(self.verify.is_first_class_keyword('PROPERTIES'))
        self.assertTrue(self.verify.is_first_class_keyword(Tokens.reindent(1) + 'PROPERTY'))
        self.assertFalse(self.verify.is_first_class_keyword('PROPERTY2'))
        self.assertFalse(self.verify.is_first_class_keyword('proPERTY'))

    def test_available_properties_version(self):
        self.assertEqual('3.17.0', self.verify.get_cmake_properties_version())

    def test_cmake_properties_matching_exactly(self):
        self.assertTrue(self.verify.is_property('LINK_DIRECTORIES'))
        self.assertTrue(self.verify.is_property('INSTALL_REMOVE_ENVIRONMENT_RPATH'))
        self.assertFalse(self.verify.is_property('1INSTALL_REMOVE_ENVIRONMENT_RPATH'))

    def test_cmake_properties_starting_with(self):
        self.assertTrue(self.verify.is_property('IMPORTED_NO_SONAME'))
        self.assertTrue(self.verify.is_property('IMPORTED_NO_SONAME_123'))
        self.assertFalse(self.verify.is_property('IMPORTED_NO_SONAME123'))
        self.assertFalse(self.verify.is_property('123_IMPORTED_NO_SONAME_123'))
        self.assertFalse(self.verify.is_property('IMPORTED_NO_SONAM'))

    def test_cmake_properties_ending_with(self):
        self.assertTrue(self.verify.is_property('_OUTPUT_NAME'))
        self.assertTrue(self.verify.is_property('VALUE_OUTPUT_NAME'))
        self.assertFalse(self.verify.is_property('_OUTPUT_NAME_VALUE'))
