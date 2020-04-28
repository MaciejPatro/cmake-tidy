###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.lexical_data import KeywordVerifier


class InvocationRealignModifier:
    __DIFF_BETWEEN_KEYWORD_AND_VALUE = 2

    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__verifier = KeywordVerifier(settings)
        self.__settings = settings

    def realign(self, invocation: dict) -> list:
        invocation['arguments'] = self.__realign_properties_if_needed(invocation['arguments'])
        invocation['arguments'] = self.__realign_double_keywords(invocation['arguments'])
        invocation['arguments'] = self.__realign_get_property(invocation)
        return self.__realign_keyword_values_if_needed(invocation['arguments'])

    def __realign_properties_if_needed(self, args: List[str]) -> list:
        return self.__realign_properties(args) if self.__should_realign_properties() else args

    def __should_realign_properties(self) -> bool:
        return self.__settings['keep_property_and_value_in_one_line'] and self.__state['has_first_class_keyword']

    def __realign_properties(self, args: List[str]) -> list:
        for i in range(len(args) - 1):
            if self.__is_property(args[i]) and args[i + 1].startswith('\n'):
                args[i + 1] = ' '
        return args

    def __is_property(self, argument: str) -> bool:
        return not self.__verifier.is_first_class_keyword(argument) and self.__verifier.is_keyword_or_property(argument)

    def __realign_double_keywords(self, args: List[str]) -> list:
        for i in range(len(args) - self.__DIFF_BETWEEN_KEYWORD_AND_VALUE):
            if self.__verifier.is_double_keyword(args[i], args[i + self.__DIFF_BETWEEN_KEYWORD_AND_VALUE]):
                args[i + 1] = ' '
        return args

    def __realign_get_property(self, invocation: dict) -> list:
        if invocation['function_name'].startswith('get_property'):
            return self.__replace_newline_with_space_after_property_keyword(invocation['arguments'])
        return invocation['arguments']

    @staticmethod
    def __replace_newline_with_space_after_property_keyword(args: List[str]) -> list:
        for i in range(len(args)):
            if KeywordVerifier.is_first_class_keyword(args[i]):
                args[i + 1] = ' '
        return args

    def __realign_keyword_values_if_needed(self, args: List[str]) -> list:
        return self.__realign_keyword_values(args) if self.__should_realign_keyword_values(args) else args

    def __should_realign_keyword_values(self, args: List[str]) -> bool:
        return self.__settings['keyword_and_single_value_in_one_line'] and \
               len(args) > InvocationRealignModifier.__DIFF_BETWEEN_KEYWORD_AND_VALUE

    def __realign_keyword_values(self, args: List[str]) -> list:
        for i in range(len(args) - InvocationRealignModifier.__DIFF_BETWEEN_KEYWORD_AND_VALUE):
            if self.__self_should_realign_value_after_keyword(args, i):
                args[i + 1] = ' '
        return args

    def __self_should_realign_value_after_keyword(self, args: List[str], current_index: int) -> bool:
        return self.__verifier.is_keyword_or_property(args[current_index]) and \
               args[current_index + 1].startswith('\n') and \
               not self.__verifier.is_keyword_or_property(args[current_index + 2]) and \
               self.__is_single_value(args, current_index)

    def __is_single_value(self, args: List[str], current_index: int) -> bool:
        tokens_diff = 4  # keyword, space, value, space, keyword
        return current_index + tokens_diff >= len(args) or \
               self.__verifier.is_keyword_or_property(args[current_index + tokens_diff])
