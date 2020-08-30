###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.formatting.utils import FormatNewline
from cmake_tidy.formatting.utils.tokens import Tokens


class NewCommandFormatter:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def format(self, invocation: dict) -> str:
        formatted = self.__format(invocation)
        return formatted

    def __format(self, invocation):
        return invocation['function_name'] + \
               self.__handle_arguments(invocation['arguments']) + \
               self.__get_formatted_closing_parenthesis()

    def __handle_arguments(self, args: List[str]) -> str:
        if self.__settings['wrap_short_invocations_to_single_line']:
            args = map(lambda token: ' ' if Tokens.is_spacing_token(token) else token, args)
        return ''.join(args)

    def __get_formatted_closing_parenthesis(self):
        if self.__settings['closing_parentheses_in_newline_when_split']:
            return FormatNewline(self.__state, self.__settings)(1) + ')'
        return ')'
