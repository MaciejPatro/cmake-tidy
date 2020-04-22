###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re

from cmake_tidy.lexical_data import KeywordVerifier


class FormatStartCommandInvocation:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data: str) -> str:
        self.__update_state(data)
        return self.__format_data(data)

    def __update_state(self, data: str):
        if KeywordVerifier.is_conditional_invocation(data):
            self.__state['indent'] += 1
        self.__state['indent'] += 1

    def __format_data(self, original: str) -> str:
        formatted = self.__remove_whitespaces_after_name(original)
        formatted = self.__unify_command_name(formatted)
        return self.__add_spacing_if_needed(formatted)

    def __unify_command_name(self, formatted: str) -> str:
        if self.__settings.get('force_command_lowercase'):
            return formatted.lower()
        return formatted

    def __add_spacing_if_needed(self, formatted: str) -> str:
        if self.__is_spacing_needed(formatted):
            return formatted.replace('(', ' (')
        return formatted

    def __is_spacing_needed(self, formatted: str) -> bool:
        return self.__settings.get('space_between_command_and_begin_parentheses') or \
               self.__should_add_space_for_conditional(formatted)

    def __should_add_space_for_conditional(self, formatted: str) -> bool:
        return self.__settings.get('space_after_loop_condition') and \
               KeywordVerifier.is_conditional_invocation(formatted)

    @staticmethod
    def __remove_whitespaces_after_name(original: str) -> str:
        formatted = re.sub(r'\s+', '', original)
        return formatted
