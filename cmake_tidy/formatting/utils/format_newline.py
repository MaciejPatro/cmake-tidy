###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.single_indent import get_single_indent
from cmake_tidy.formatting.utils.tokens import Tokens


class FormatNewline:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data) -> str:
        return self.__format_newlines(data) + self.__prepare_initial_newline_indent()

    def __prepare_initial_newline_indent(self) -> str:
        return self.__state['indent'] * get_single_indent(self.__settings)

    def __format_newlines(self, number_of_newlines: int) -> str:
        return Tokens.remove_spaces() + '\n' * min(self.__settings['succeeding_newlines'], number_of_newlines)
