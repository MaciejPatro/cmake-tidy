###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re

from cmake_tidy.formatting.utils.tokens import Tokens


class FormatStartCommandInvocation:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data: str) -> str:
        self.__state['indent'] += 1
        return self.__format_data(data)

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
               (self.__settings.get('space_after_loop_condition') and self.__is_conditional(formatted))

    @staticmethod
    def __is_conditional(formatted: str) -> bool:
        return any([token == formatted[:-1] for token in Tokens.conditional_tokens()])

    @staticmethod
    def __remove_whitespaces_after_name(original: str) -> str:
        formatted = re.sub(r'\s+', '', original)
        return formatted
