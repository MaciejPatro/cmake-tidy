import re

from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.utils.keyword_verifier import KeywordVerifier

_newline_pattern = re.compile(r'\A\s\s+\Z')


class FormatCommandInvocation:
    __start_tokens = ['macro', 'while', 'foreach', 'if', 'function']
    __reindent_commands = ['endfunction', 'endif', 'elseif', 'endwhile', 'endforeach', 'endmacro',
                           'else']

    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings
        self.__verifier = KeywordVerifier(settings)

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
        if not self.__is_start_of_special_command(function_name):
            self.__state['indent'] -= 1
        if self.__is_end_of_special_command(function_name):
            self.__state['indent'] -= 1
        self.__state['keyword_argument'] = False

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
        command_invocation = self.__wrap_invocation(invocation)
        if self.__is_fitting_in_line(command_invocation):
            return command_invocation['arguments']
        else:
            return invocation['arguments']

    def __is_fitting_in_line(self, command_invocation: dict) -> bool:
        length = self.__invocation_length(command_invocation)
        return length < self.__settings['line_length']

    def __invocation_length(self, command_invocation: dict) -> int:
        return len(self.__join_command_invocation(command_invocation)) + \
               len(self.__newline_indent()) - \
               len(Tokens.reindent)

    def __newline_indent(self) -> str:
        indent = max(self.__state['indent'] - 1, 0)
        return indent * self.__settings['tab_size'] * ' '

    @staticmethod
    def __wrap_invocation(invocation: dict) -> dict:
        wrapped_invoke = FormatCommandInvocation.__prepare_wrapped_invocation(invocation)
        wrapped_invoke['arguments'] = [e if not _newline_pattern.match(e) else ' ' for e in wrapped_invoke['arguments']]
        return wrapped_invoke

    @staticmethod
    def __prepare_wrapped_invocation(invocation: dict) -> dict:
        new_invoke = invocation.copy()
        if _newline_pattern.match(new_invoke['arguments'][0]):
            new_invoke['arguments'] = new_invoke['arguments'][1:]
        return new_invoke

    def __is_wrappable(self, invocation: dict) -> bool:
        return len(invocation['arguments']) > 0 and self.__settings['wrap_short_invocations_to_single_line'] is True

    def __split_command_to_newlines(self, invocation: dict) -> list:
        initial_indent = self.__state['indent']
        arguments = []
        for arg in invocation['arguments']:
            newline = FormatNewline(self.__state, self.__settings)(1)
            if arg is ' ':
                arguments.append(newline)
            else:
                if self.__verifier.is_keyword(arg):
                    self.__state['indent'] = initial_indent + 1
                arguments.append(arg)
        self.__state['indent'] = initial_indent
        return arguments

    @staticmethod
    def __join_command_invocation(invocation: dict) -> str:
        formatted = invocation['function_name'] + ''.join(invocation['arguments']) + invocation['closing']
        return formatted

    def __add_reindent_tokens_where_needed(self, data: str) -> str:
        for token in FormatCommandInvocation.__reindent_commands:
            if self.__matches(token, data):
                return Tokens.reindent + data
        return data

    @staticmethod
    def __matches(token: str, data: str) -> bool:
        return re.match(r'^' + re.escape(token) + r'\s?\(', data) is not None
