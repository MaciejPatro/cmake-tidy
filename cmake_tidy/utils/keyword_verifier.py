import re


class KeywordVerifier:
    def __init__(self, settings: dict):
        self.__settings = settings

    def is_keyword(self, data: str) -> bool:
        return self.__is_one_of_defined_keywords(data) or \
               self.__should_be_handled_as_keyword(data) or \
               data == 'PROPERTIES' or \
               data == 'PROPERTY'

    def __is_one_of_defined_keywords(self, data: str) -> bool:
        return self.__settings.get('keywords') and data in self.__settings.get('keywords')

    def __should_be_handled_as_keyword(self, data: str) -> bool:
        return self.__settings.get('unquoted_uppercase_as_keyword') and re.match(r'^[A-Z]+$', data)
