###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re

from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.lexical_data import KeywordVerifier


class CommandInvocationStateUpdater:
    def __init__(self, state: dict):
        self.__state = state

    def update_state(self, function_name: str) -> None:
        self.__update_indent_state(function_name)
        self.__state['keyword_argument'] = False
        self.__state['has_first_class_keyword'] = False

    def __update_indent_state(self, function_name: str) -> None:
        if not self.__is_start_of_special_command(function_name):
            self.__state['indent'] -= 1
        if self.__state['has_first_class_keyword']:
            self.__state['indent'] -= 1
        if self.__is_end_of_special_command(function_name):
            self.__state['indent'] -= 1
        if KeywordVerifier.is_conditional_invocation(function_name):
            self.__state['indent'] -= 1

    def __is_start_of_special_command(self, original: str) -> bool:
        return any([self.__matches(token, original.lower()) for token in Tokens.start_tokens()])

    def __is_end_of_special_command(self, original: str) -> bool:
        return any([self.__matches(token, original.lower()) for token in Tokens.end_tokens()])

    @staticmethod
    def __matches(token: str, data: str) -> bool:
        return re.match(r'^' + re.escape(token) + r'\s?\(', data) is not None
