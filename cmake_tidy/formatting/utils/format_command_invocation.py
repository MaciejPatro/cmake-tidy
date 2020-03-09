###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################
import re

from cmake_tidy.formatting.utils.invocation_splitter import InvocationSplitter
from cmake_tidy.formatting.utils.invocation_wrapper import InvocationWrapper
from cmake_tidy.formatting.utils.single_indent import get_single_indent
from cmake_tidy.formatting.utils.tokens import Tokens


class FormatCommandInvocation:
    __start_tokens = ['macro', 'while', 'foreach', 'if', 'function']
    __reindent_commands = ['endfunction', 'endif', 'elseif', 'endwhile', 'endforeach', 'endmacro',
                           'else']

    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data: list) -> str:
        command_invocation = self.__prepare_data(data)
        formatted = self.__format_invocation(command_invocation)
        self.__update_state(command_invocation['function_name'])
        return formatted

    @staticmethod
    def __prepare_data(data: list) -> dict:
        return {'function_name': data[0],
                'arguments': data[1] if len(data) == 3 else [],
                'closing': data[2] if len(data) == 3 else data[1]}

    def __update_state(self, function_name: str) -> None:
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

    def __is_start_of_special_command(self, original: str) -> bool:
        return any([self.__matches(token, original) for token in FormatCommandInvocation.__start_tokens])

    def __is_end_of_special_command(self, original: str) -> bool:
        return any([self.__matches('end' + token, original) for token in FormatCommandInvocation.__start_tokens])

    def __format_invocation(self, invocation: dict) -> str:
        invocation['arguments'] = self.__prepare_arguments(invocation)
        formatted = self.__join_command_invocation(invocation)
        return self.__add_reindent_tokens_where_needed(formatted)

    def __prepare_arguments(self, invocation: dict) -> list:
        if self.__is_wrappable(invocation):
            invocation['arguments'] = self.__wrap_arguments_if_possible(invocation)
        if not self.__is_fitting_in_line(invocation):
            invocation['arguments'] = self.__split_command_to_newlines(invocation)
        return invocation['arguments']

    def __wrap_arguments_if_possible(self, invocation: dict) -> list:
        command_invocation = InvocationWrapper().wrap(invocation)
        if self.__is_fitting_in_line(command_invocation):
            return command_invocation['arguments']
        else:
            return invocation['arguments']

    def __is_fitting_in_line(self, command_invocation: dict) -> bool:
        return self.__invocation_length(command_invocation) < self.__settings['line_length']

    def __invocation_length(self, command_invocation: dict) -> int:
        invoke = self.__join_command_invocation(command_invocation) + self.__newline_indent()
        invoke = invoke.replace('\t', ' ' * self.__settings['tab_size'])
        return len(invoke) - len(Tokens.reindent(1))

    def __newline_indent(self) -> str:
        indent = max(self.__state['indent'] - 1, 0)
        return indent * get_single_indent(self.__settings)

    def __is_wrappable(self, invocation: dict) -> bool:
        return len(invocation['arguments']) > 0 and self.__settings['wrap_short_invocations_to_single_line'] is True

    def __split_command_to_newlines(self, invocation: dict) -> list:
        return InvocationSplitter(self.__state, self.__settings).split(invocation)

    @staticmethod
    def __join_command_invocation(invocation: dict) -> str:
        formatted = invocation['function_name'] + ''.join(invocation['arguments']) + invocation['closing']
        return formatted

    def __add_reindent_tokens_where_needed(self, data: str) -> str:
        for token in FormatCommandInvocation.__reindent_commands:
            if self.__matches(token, data):
                return Tokens.reindent(1) + data
        return data

    @staticmethod
    def __matches(token: str, data: str) -> bool:
        return re.match(r'^' + re.escape(token) + r'\s?\(', data) is not None
