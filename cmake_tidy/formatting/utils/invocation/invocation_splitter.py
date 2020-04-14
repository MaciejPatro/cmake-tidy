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
        arguments = self.__split_args_to_newlines(invocation)
        arguments = self.__fix_line_comments(arguments)
        arguments = self.__realign(arguments)
        return arguments + self.__add_closing_bracket_separator(invocation)

    def __realign(self, arguments: List[str]) -> list:
        arguments = self.__realign_properties_if_needed(arguments)
        return self.__realign_keyword_values_if_needed(arguments)

    def __split_args_to_newlines(self, invocation: dict) -> list:
        return [self.__handle_argument(arg) for arg in invocation['arguments']]

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

    def __realign_properties_if_needed(self, arguments: List[str]) -> list:
        return self.__realign_properties(arguments) if self.__should_realign_properties() else arguments

    def __realign_properties(self, arguments: List[str]) -> list:
        for i in range(len(arguments) - 1):
            if self.__is_property(arguments[i]) and arguments[i + 1].startswith('\n'):
                arguments[i + 1] = ' '
        return arguments

    def __should_realign_properties(self) -> bool:
        return self.__settings['keep_property_and_value_in_one_line'] and self.__state['has_first_class_keyword']

    def __is_property(self, argument: str) -> bool:
        return not self.__verifier.is_first_class_keyword(argument) and self.__verifier.is_keyword_or_property(argument)

    def __realign_keyword_values_if_needed(self, arguments: List[str]) -> list:
        return self.__realign_keyword_values(arguments) if self.__should_realign_keyword_values(
            arguments) else arguments

    def __should_realign_keyword_values(self, arguments):
        return self.__settings['keyword_and_single_value_in_one_line'] and len(arguments) > 3

    def __realign_keyword_values(self, arguments):
        # TODO: put implementation here
        return arguments

    @staticmethod
    def __fix_line_comments(arguments: list) -> list:
        for i in range(len(arguments)):
            if arguments[i].startswith('#'):
                arguments[i - 1] = ' '
        return arguments
