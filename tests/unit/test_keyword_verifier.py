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
        self.settings = {'keywords': ['some'], 'unquoted_uppercase_as_keyword': False}
        self.verify = KeywordVerifier(self.settings)

    @mock.patch('builtins.open')
    def test_ensure_properties_are_read_only_once(self, mock_open: MagicMock):
        self.verify = KeywordVerifier(self.settings)
        self.assertFalse(mock_open.called)

    def test_should_accept_keyword_when_on_the_list(self):
        self.assertTrue(self.verify.is_keyword('some'))
        self.assertTrue(self.verify.is_keyword(Tokens.reindent(1) + 'some'))
        self.assertFalse(self.verify.is_keyword('some2'))
        self.assertFalse(self.verify.is_keyword('${some}'))

    def test_unquoted_arguments_with_uppercase_letters_only_are_keywords(self):
        self.settings['unquoted_uppercase_as_keyword'] = True
        self.verify = KeywordVerifier(self.settings)

        self.assertTrue(self.verify.is_keyword('OTHER'))
        self.assertTrue(self.verify.is_keyword(Tokens.reindent(1) + 'OTHER'))
        self.assertTrue(self.verify.is_keyword('WITH_SEPARATION'))

        self.assertFalse(self.verify.is_keyword('"$OTHER"'))
        self.assertFalse(self.verify.is_keyword('SOMeARG'))
        self.assertFalse(self.verify.is_keyword('a_ARGUMENT'))
        self.assertFalse(self.verify.is_keyword('NOT_'))
        self.assertFalse(self.verify.is_keyword('_SOME'))

    def test_whether_token_is_first_class_keyword(self):
        self.assertTrue(self.verify.is_first_class_keyword('PROPERTY'))
        self.assertTrue(self.verify.is_first_class_keyword('PROPERTIES'))
        self.assertTrue(self.verify.is_first_class_keyword(Tokens.reindent(1) + 'PROPERTY'))
        self.assertFalse(self.verify.is_first_class_keyword('PROPERTY2'))
        self.assertFalse(self.verify.is_first_class_keyword('proPERTY'))

    def test_available_properties_version(self):
        self.assertEqual('3.18.0', self.verify.get_cmake_properties_version())

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

    def test_cmake_properties_with_reindent_token(self):
        self.assertTrue(self.verify.is_property(Tokens.reindent(1) + 'LINK_DIRECTORIES'))

    def test_double_keywords(self):
        self.assertTrue(self.verify.is_double_keyword(Tokens.reindent(1) + 'RUNTIME', 'DESTINATION'))
        self.assertTrue(self.verify.is_double_keyword('ARCHIVE', Tokens.reindent(1) + 'DESTINATION'))
        self.assertTrue(self.verify.is_double_keyword('LIBRARY', 'DESTINATION'))
        self.assertFalse(self.verify.is_double_keyword('OUTPUT', 'DESTINATION'))
        self.assertFalse(self.verify.is_double_keyword('LIBRARY', 'OUTPUT'))

    def test_recognition_of_conditional_invocation(self):
        self.assertTrue(KeywordVerifier.is_conditional_invocation('If('))
        self.assertTrue(KeywordVerifier.is_conditional_invocation('while('))
        self.assertTrue(KeywordVerifier.is_conditional_invocation('while ('))
        self.assertFalse(KeywordVerifier.is_conditional_invocation('foreach ('))
        self.assertFalse(KeywordVerifier.is_conditional_invocation('if2('))
        self.assertFalse(KeywordVerifier.is_conditional_invocation('if*'))

    def test_is_command_keyword(self):
        self.assertTrue(KeywordVerifier.is_command_keyword('COMMAND'))
        self.assertTrue(KeywordVerifier.is_command_keyword(Tokens.reindent(1) + 'COMMAND'))
        self.assertTrue(KeywordVerifier.is_command_keyword(Tokens.reindent(1) + 'ARGS'))
        self.assertFalse(KeywordVerifier.is_command_keyword('CMD'))
        self.assertFalse(KeywordVerifier.is_command_keyword(Tokens.reindent(2) + 'COMMAND'))
