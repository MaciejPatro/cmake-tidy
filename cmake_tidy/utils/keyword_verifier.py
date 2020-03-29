###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re

from cmake_tidy.formatting.utils.tokens import Tokens


class KeywordVerifier:
    __FIRST_CLASS_KEYWORDS = ['PROPERTIES', 'PROPERTY']

    def __init__(self, settings: dict):
        self.__settings = settings

    @staticmethod
    def is_first_class_keyword(data: str) -> bool:
        data = data.replace(Tokens.reindent(1), '')
        return data in KeywordVerifier.__FIRST_CLASS_KEYWORDS

    def is_keyword(self, data: str) -> bool:
        data = data.replace(Tokens.reindent(1), '')
        return self.__is_one_of_defined_keywords(data) or \
               self.__should_be_handled_as_keyword(data) or \
               self.is_first_class_keyword(data)

    def __is_one_of_defined_keywords(self, data: str) -> bool:
        return self.__settings.get('keywords') and data in self.__settings.get('keywords')

    def __should_be_handled_as_keyword(self, data: str) -> bool:
        return self.__settings.get('unquoted_uppercase_as_keyword') and re.match(r'^[A-Z]+$', data)
