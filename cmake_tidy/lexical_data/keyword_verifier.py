###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import json
import re
from pathlib import Path

from cmake_tidy.formatting.utils.tokens import Tokens


class KeywordVerifier:
    __FIRST_CLASS_KEYWORDS = ['PROPERTIES', 'PROPERTY']
    __PROPERTIES = dict()

    @staticmethod
    def __init_properties():
        if not KeywordVerifier.__PROPERTIES:
            with (Path(__file__).parent / 'keyword_list.json').open() as file:
                KeywordVerifier.__PROPERTIES = json.load(file)

    def __init__(self, settings: dict):
        KeywordVerifier.__init_properties()
        self.__settings = settings

    @staticmethod
    def is_first_class_keyword(data: str) -> bool:
        data = data.replace(Tokens.reindent(1), '')
        return data in KeywordVerifier.__FIRST_CLASS_KEYWORDS

    def get_cmake_properties_version(self) -> str:
        return self.__PROPERTIES["cmake_version"]

    def is_keyword_or_property(self, data: str) -> bool:
        return self.is_property(data) or self.is_keyword(data)

    def is_keyword(self, data: str) -> bool:
        data = data.replace(Tokens.reindent(1), '')
        return self.__is_one_of_defined_keywords(data) or \
               self.__should_be_handled_as_keyword(data) or \
               self.is_first_class_keyword(data) or \
               self.__is_keyword_in_cmake(data)

    @staticmethod
    def is_conditional_invocation(data: str) -> bool:
        data = data.lower().replace(' ', '')
        return any([token == data[:-1] for token in Tokens.conditional_tokens()]) and data[-1] == '('

    @staticmethod
    def is_double_keyword(first: str, second: str) -> bool:
        first = first.replace(Tokens.reindent(1), '')
        second = second.replace(Tokens.reindent(1), '')
        return any(keyword.startswith(first) and keyword.endswith(second) \
                   for keyword in KeywordVerifier.__PROPERTIES['double-keywords'])

    @staticmethod
    def is_command_keyword(data: str) -> bool:
        data = data.replace(Tokens.reindent(1), '')
        return data == 'COMMAND' or data == 'ARGS'

    def __is_one_of_defined_keywords(self, data: str) -> bool:
        return self.__settings.get('keywords') and data in self.__settings['keywords']

    def __should_be_handled_as_keyword(self, data: str) -> bool:
        upper_case_regex = r'^([A-Z]+_?)+[A-Z]$'
        return self.__settings.get('unquoted_uppercase_as_keyword') and re.match(upper_case_regex, data)

    def is_property(self, data: str) -> bool:
        data = data.replace(Tokens.reindent(1), '')
        return data in KeywordVerifier.__PROPERTIES["properties_full_names"] or \
               self.__is_property_regex_starting(data) or \
               self.__is_property_ending_with(data)

    @staticmethod
    def __is_keyword_in_cmake(data: str) -> bool:
        return any([data in KeywordVerifier.__PROPERTIES["keywords"]])

    @staticmethod
    def __is_property_ending_with(data: str) -> bool:
        return any([data.endswith(token) for token in KeywordVerifier.__PROPERTIES['properties_ending_with']])

    @staticmethod
    def __is_property_regex_starting(data: str) -> bool:
        return any([data.startswith(token) for token in KeywordVerifier.__PROPERTIES['properties_starting_with']])
