###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.formatting.utils import FormatNewline


class NewCommandFormatter:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings
        self.__newline_formatter = FormatNewline(state, settings)

    def format(self, invocation: dict) -> str:
        return invocation['function_name'] + self.handle_arguments(invocation['arguments']) + invocation['closing']

    def handle_arguments(self, args: List[str]) -> str:
        return self.__newline_formatter(1).join(args)
