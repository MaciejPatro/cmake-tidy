###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.updaters.keyword_state_updater import KeywordStateUpdater
from cmake_tidy.lexical_data import KeywordVerifier


class InvocationSplitter:
    __DIFF_BETWEEN_KEYWORD_AND_VALUE = 2

    def __init__(self, state: dict, settings: dict):
        self.__prepare_state(state)
        self.__state_updater = KeywordStateUpdater(self.__state, settings)
        self.__verifier = KeywordVerifier(settings)
        self.__settings = settings

    def split(self, invocation: dict) -> list:
        args = self.__split_args_to_newlines(invocation)
        args = self.__fix_line_comments(args)
        args = self.__realign(args)
        return args + self.__add_closing_bracket_separator(invocation)

    def __realign(self, args: List[str]) -> list:
        args = self.__realign_properties_if_needed(args)
        return self.__realign_keyword_values_if_needed(args)

    def __split_args_to_newlines(self, invocation: dict) -> list:
        return list(filter(len, [self.__handle_argument(arg) for arg in invocation['arguments']]))

    def __handle_argument(self, arg: str) -> str:
        self.__state_updater.update_state(arg)
        return self.__get_converted_whitespace() if arg == ' ' else arg

    def __add_closing_bracket_separator(self, invocation: dict) -> list:
        if self.__settings['closing_parentheses_in_newline_when_split'] and \
                not self.__is_last_element_newline(invocation):
            return [FormatNewline(self.__state, self.__settings)(1)]
        return []

    @staticmethod
    def __is_last_element_newline(invocation: dict) -> bool:
        return invocation['arguments'][-1].startswith('\n')

    def __get_converted_whitespace(self) -> str:
        return FormatNewline(self.__state, self.__settings)(1)

    def __prepare_state(self, state: dict) -> None:
        self.__state = state.copy()
        if self.__state['has_first_class_keyword']:
            self.__state['indent'] -= 1
        self.__state['has_first_class_keyword'] = False
        self.__state['keyword_argument'] = False

    def __realign_properties_if_needed(self, args: List[str]) -> list:
        return self.__realign_properties(args) if self.__should_realign_properties() else args

    def __realign_properties(self, args: List[str]) -> list:
        for i in range(len(args) - 1):
            if self.__is_property(args[i]) and args[i + 1].startswith('\n'):
                args[i + 1] = ' '
        return args

    def __should_realign_properties(self) -> bool:
        return self.__settings['keep_property_and_value_in_one_line'] and self.__state['has_first_class_keyword']

    def __is_property(self, argument: str) -> bool:
        return not self.__verifier.is_first_class_keyword(argument) and self.__verifier.is_keyword_or_property(argument)

    def __realign_keyword_values_if_needed(self, args: List[str]) -> list:
        return self.__realign_keyword_values(args) if self.__should_realign_keyword_values(args) else args

    def __should_realign_keyword_values(self, args: List[str]) -> bool:
        return self.__settings['keyword_and_single_value_in_one_line'] and \
               len(args) > InvocationSplitter.__DIFF_BETWEEN_KEYWORD_AND_VALUE

    def __realign_keyword_values(self, args: List[str]) -> list:
        for i in range(len(args) - InvocationSplitter.__DIFF_BETWEEN_KEYWORD_AND_VALUE):
            if self.__self_should_realign_value_after_keyword(args, i):
                args[i + 1] = ' '
        return args

    def __self_should_realign_value_after_keyword(self, args: List[str], current_index: int) -> bool:
        return self.__verifier.is_keyword_or_property(args[current_index]) and \
               args[current_index + 1].startswith('\n') and \
               not self.__verifier.is_keyword_or_property(args[current_index + 2]) and \
               self.__is_single_value(args, current_index)

    def __is_single_value(self, args, current_index):
        tokens_diff = 4  # keyword, space, value, space, keyword
        return current_index + tokens_diff >= len(args) or \
               self.__verifier.is_keyword_or_property(args[current_index + tokens_diff])

    @staticmethod
    def __fix_line_comments(args: list) -> list:
        for i in range(len(args)):
            if args[i].startswith('#'):
                args[i - 1] = ' '
        return args
