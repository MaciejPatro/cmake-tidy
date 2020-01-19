import re

from cmake_tidy.formatting.utils.tokens import Tokens


class FormatCommandInvocation:
    __start_tokens = ['macro', 'while', 'foreach', 'if', 'function']
    __reindent_commands = ['endfunction', 'endif', 'elseif', 'endwhile', 'endforeach', 'endmacro',
                           'else']

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        self.__update_state(data[0])
        if len(data) == 2:
            original = data[0] + data[1]
        else:
            original = data[0] + ''.join(data[1]) + data[2]
        return self.__add_reindent_tokens_where_needed(original)

    def __update_state(self, function_name):
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
    def __matches(token, data) -> bool:
        return re.match(r'^' + re.escape(token) + r'\s?\(', data) is not None
