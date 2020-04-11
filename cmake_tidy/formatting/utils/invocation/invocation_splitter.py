###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.updaters.keyword_state_updater import KeywordStateUpdater
from cmake_tidy.lexical_data import KeywordVerifier


class InvocationSplitter:
    def __init__(self, state: dict, settings: dict):
        self.__prepare_state(state)
        self.__state_updater = KeywordStateUpdater(self.__state, settings)
        self.__verifier = KeywordVerifier(settings)
        self.__settings = settings

    def split(self, invocation: dict) -> list:
        arguments = self.__split_args_to_newlines(invocation) + self.__add_closing_bracket_separator()
        arguments = self.__fix_line_comments(arguments)
        arguments = self.__realign_properties(arguments)
        return arguments

    def __split_args_to_newlines(self, invocation: dict) -> list:
        return [self.__handle_argument(arg) for arg in invocation['arguments']]

    def __handle_argument(self, arg: str) -> str:
        self.__state_updater.update_state(arg)
        return self.__get_converted_whitespace() if arg == ' ' else arg

    def __add_closing_bracket_separator(self) -> list:
        if self.__settings['closing_parentheses_in_newline_when_split']:
            return [FormatNewline(self.__state, self.__settings)(1)]
        return []

    def __get_converted_whitespace(self) -> str:
        return FormatNewline(self.__state, self.__settings)(1)

    def __prepare_state(self, state: dict) -> None:
        self.__state = state.copy()
        if self.__state['has_first_class_keyword']:
            self.__state['indent'] -= 1
        self.__state['has_first_class_keyword'] = False
        self.__state['keyword_argument'] = False

    def __realign_properties(self, arguments: List[str]) -> list:
        if not self.__should_realign():
            return arguments
        for i in range(len(arguments) - 1):
            if self.__is_property(arguments[i]) and arguments[i + 1].startswith('\n'):
                arguments[i + 1] = ' '
        return arguments

    def __should_realign(self) -> bool:
        return self.__settings['keep_property_and_value_in_one_line'] and self.__state['has_first_class_keyword']

    def __is_property(self, argument: str) -> bool:
        return not self.__verifier.is_first_class_keyword(argument) and self.__verifier.is_keyword_or_property(argument)

    @staticmethod
    def __fix_line_comments(arguments: list) -> list:
        for i in range(len(arguments)):
            if arguments[i].startswith('#'):
                arguments[i-1] = ' '
        return arguments
