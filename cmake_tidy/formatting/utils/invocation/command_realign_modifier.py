###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List, Tuple

from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.lexical_data import KeywordVerifier


class CommandRealignModifier:
    __DIFF_BETWEEN_KEYWORD_AND_VALUE = 2

    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__verifier = KeywordVerifier(settings)
        self.__settings = settings

    def realign(self, invocation: dict) -> list:
        invocation['arguments'] = self.__realign_properties_if_needed(invocation['arguments'])
        invocation['arguments'] = self.__realign_double_keywords(invocation['arguments'])
        invocation['arguments'] = self.__realign_get_property(invocation)
        invocation['arguments'] = self.__realign_set_property(invocation)
        invocation['arguments'] = self.__realign_commands_if_needed(invocation['arguments'])
        return self.__realign_keyword_values_if_needed(invocation['arguments'])

    def __realign_commands_if_needed(self, args: List[str]) -> list:
        return self.__realign_commands(args) if self.__settings.get('keep_command_in_single_line') else args

    def __realign_commands(self, args: List[str]) -> list:
        diff = 0 if self.__settings.get('keyword_and_single_value_in_one_line') else CommandRealignModifier.__DIFF_BETWEEN_KEYWORD_AND_VALUE
        for i in range(len(args)):
            if KeywordVerifier.is_command_keyword(args[i]):
                for j in range(i + diff, len(args) - 1):
                    if self.__verifier.is_keyword(args[j + 1]):
                        break
                    if Tokens.is_spacing_token(args[j]):
                        args[j] = ' '
        return args

    def __realign_properties_if_needed(self, args: List[str]) -> list:
        return self.__realign_properties(args) if self.__should_realign_properties() else args

    def __should_realign_properties(self) -> bool:
        return self.__settings['keep_property_and_value_in_one_line'] and self.__state['has_first_class_keyword']

    def __realign_properties(self, args: List[str]) -> list:
        for i in range(len(args) - 2):
            if self.__is_property(args[i]) and self.__should_realign_value_after_keyword(args, i):
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

    def __realign_set_property(self, invocation: dict) -> list:
        if invocation['function_name'].startswith('set_property'):
            return self.__realign_property_in_set_function(invocation['arguments'])
        return invocation['arguments']

    def __realign_property_in_set_function(self, args: List[str]) -> list:
        for i in range(len(args)):
            if KeywordVerifier.is_first_class_keyword(args[i]):
                args, position = self.__reindent_property_name(args, i)
                if self.__is_possible_to_realign_keyword_values(args) and self.__is_value_realignable(args, position):
                    args[position + 1] = ' '
        return args

    def __is_value_realignable(self, args, position):
        return not Tokens.is_line_comment(args[position + 2]) and \
               self.__get_number_of_arguments(args, position) == 1

    def __get_number_of_arguments(self, args: List[str], start: int) -> int:
        return sum([self.__is_argument(data) for data in args[start + 1:]])

    def __reindent_property_name(self, args: list, start_index: int) -> Tuple[list, int]:
        for i in range(start_index + 1, len(args)):
            if self.__is_argument(args[i]):
                if not args[i].startswith(Tokens.reindent(1)):
                    args[i] = Tokens.reindent(1) + args[i]
                return args, i
        return args, 0

    @staticmethod
    def __is_argument(data: str) -> bool:
        return not (Tokens.is_line_comment(data) or Tokens.is_spacing_token(data))

    def __replace_newline_with_space_after_property_keyword(self, args: List[str]) -> list:
        for i in range(len(args) - CommandRealignModifier.__DIFF_BETWEEN_KEYWORD_AND_VALUE):
            if self.__is_property_followed_by_name(args, i):
                args[i + 1] = ' '
        return args

    def __realign_keyword_values_if_needed(self, args: List[str]) -> list:
        return self.__realign_keyword_values(args) if self.__is_possible_to_realign_keyword_values(args) else args

    def __is_possible_to_realign_keyword_values(self, args: List[str]) -> bool:
        return self.__settings['keyword_and_single_value_in_one_line'] and \
               len(args) > CommandRealignModifier.__DIFF_BETWEEN_KEYWORD_AND_VALUE

    def __realign_keyword_values(self, args: List[str]) -> list:
        for i in range(len(args) - CommandRealignModifier.__DIFF_BETWEEN_KEYWORD_AND_VALUE):
            if self.__should_realign_value_after_keyword(args, i):
                args[i + 1] = ' '
        return args

    def __should_realign_value_after_keyword(self, args: List[str], current_index: int) -> bool:
        return self.__verifier.is_keyword_or_property(args[current_index]) and \
               Tokens.is_spacing_token(args[current_index + 1]) and \
               not self.__verifier.is_keyword_or_property(args[current_index + 2]) and \
               self.__is_single_value(args, current_index)

    def __is_single_value(self, args: List[str], current_index: int) -> bool:
        tokens_diff = 4  # keyword, space, value, space, keyword
        return current_index + tokens_diff >= len(args) or \
               self.__verifier.is_keyword_or_property(args[current_index + tokens_diff])

    @staticmethod
    def __is_property_followed_by_name(args: list, i: int) -> bool:
        return KeywordVerifier.is_first_class_keyword(args[i]) and not Tokens.is_line_comment(args[i + 2])
