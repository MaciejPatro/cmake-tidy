import re

from cmake_tidy.formatting.utils.tokens import Tokens


class FormatCommandInvocation:
    __start_tokens = ['macro', 'while', 'foreach', 'if', 'function']
    __reindent_commands = ['endfunction', 'endif', 'elseif', 'endwhile', 'endforeach', 'endmacro',
                           'else']

    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data: list) -> str:
        self.__update_state(data[0])
        return self.__format_invocation(data)

    def __format_invocation(self, data: list) -> str:
        self.__wrap_to_single_line_if_feasible(data)
        formatted = self.__join_all_tokens(data)
        return self.__add_reindent_tokens_where_needed(formatted)

    def __wrap_to_single_line_if_feasible(self, data: list) -> None:
        whitespaces_pattern = re.compile(r'\A\s\s+\Z')
        if len(data) == 3 and self.__settings['wrap_short_invocations_to_single_line'] is True:
            data[1] = [element for element in data[1] if not whitespaces_pattern.match(element)]

    @staticmethod
    def __join_all_tokens(data) -> str:
        if len(data) == 2:
            return data[0] + data[1]
        else:
            return data[0] + ''.join(data[1]) + data[2]

    def __update_state(self, function_name: str) -> None:
        if not self.__is_start_of_special_command(function_name):
            self.__state['indent'] -= 1
        if self.__is_end_of_special_command(function_name):
            self.__state['indent'] -= 1
        self.__state['keyword_argument'] = False

    def __is_start_of_special_command(self, original: str) -> bool:
        return any([self.__matches(token, original) for token in FormatCommandInvocation.__start_tokens])

    def __is_end_of_special_command(self, original: str) -> bool:
        return any([self.__matches('end' + token, original) for token in FormatCommandInvocation.__start_tokens])

    def __add_reindent_tokens_where_needed(self, data: str) -> str:
        for token in FormatCommandInvocation.__reindent_commands:
            if self.__matches(token, data):
                return Tokens.reindent + data
        return data

    @staticmethod
    def __matches(token: str, data: str) -> bool:
        return re.match(r'^' + re.escape(token) + r'\s?\(', data) is not None
