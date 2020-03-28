###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################
from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.utils.keyword_verifier import KeywordVerifier


class InvocationSplitter:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__initial_indent = self.__state['indent']
        self.__settings = settings
        self.__verifier = KeywordVerifier(settings)

    def split(self, invocation: dict) -> list:
        self.__initial_indent = self.__state['indent']
        arguments = self.__split_args_to_newlines(invocation) + self.__add_closing_bracket_separator()
        self.__rollback_indent_state()
        return arguments

    def __split_args_to_newlines(self, invocation: dict) -> list:
        arguments = []
        for arg in invocation['arguments']:
            if arg == ' ':
                arguments += self.__get_converted_whitespace()
            else:
                self.__handle_non_whitespace_arguments(arg, arguments)
        return arguments

    def __get_converted_whitespace(self) -> list:
        return [(FormatNewline(self.__state, self.__settings)(1))]

    def __rollback_indent_state(self) -> None:
        self.__state['indent'] = self.__initial_indent

    def __add_closing_bracket_separator(self) -> list:
        if self.__settings['closing_parentheses_in_newline_when_split']:
            return [FormatNewline(self.__state, self.__settings)(1)]
        return []

    def __handle_non_whitespace_arguments(self, arg: str, arguments: list) -> None:
        self.__update_indent_state(arg)
        self.__fix_line_comment(arg, arguments)
        arguments.append(arg)

    def __update_indent_state(self, arg: str):
        if self.__verifier.is_keyword(arg):
            self.__state['indent'] = self.__initial_indent + 1

    @staticmethod
    def __fix_line_comment(current_argument, arguments):
        if current_argument.startswith('#'):
            arguments[-1] = ' '
