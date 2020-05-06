###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re
from abc import ABC, abstractmethod
from typing import List

from cmake_tidy.formatting.utils.invocation.invocation_wrapper import InvocationWrapper
from cmake_tidy.formatting.utils.invocation.line_comments_formatter import LineCommentsFormatter
from cmake_tidy.formatting.utils.single_indent import get_single_indent
from cmake_tidy.formatting.utils.tokens import Tokens


class InvocationFormatter(ABC):
    def __init__(self, state: dict, settings: dict):
        self._settings = settings
        self._state = state

    @abstractmethod
    def format(self, invocation: dict) -> str:
        pass

    def _is_fitting_in_line(self, command_invocation: dict) -> bool:
        return self._invocation_length(command_invocation) < self._settings['line_length']

    def _newline_indent(self) -> str:
        indent = max(self._state['indent'] - 1, 0)
        return indent * get_single_indent(self._settings)

    def _invocation_length(self, command_invocation: dict) -> int:
        invoke = self._join_command_invocation(command_invocation) + self._newline_indent()
        invoke = invoke.replace('\t', ' ' * self._settings['tab_size'])
        invoke = re.sub(Tokens.get_reindent_regex(), '', invoke)
        invoke = re.sub(Tokens.remove_spaces(), '', invoke)
        return len(invoke)

    def _join_command_invocation(self, invocation: dict) -> str:
        formatted = invocation['function_name'] + ''.join(invocation['arguments']) + invocation['closing']
        return self.__add_reindent_tokens_where_needed(formatted)

    def _prepare_arguments(self, invocation: dict) -> list:
        invocation['arguments'] = self.__remove_empty_arguments(invocation)
        invocation['arguments'] = self.__remove_whitespace_at_end_of_line(invocation['arguments'])
        invocation['arguments'] = LineCommentsFormatter(self._state, self._settings).format(invocation['arguments'])
        if self.__is_wrappable(invocation):
            invocation['arguments'] = self.__wrap_arguments_if_possible(invocation)
        return invocation['arguments']

    @staticmethod
    def __add_reindent_tokens_where_needed(data: str) -> str:
        data_lower = data.lower()
        if any(data_lower.startswith(token) for token in Tokens.reindent_commands_tokens()):
            return Tokens.reindent(1) + data
        return data

    def __is_wrappable(self, invocation: dict) -> bool:
        return len(invocation['arguments']) > 0 and self._settings['wrap_short_invocations_to_single_line'] is True

    def __wrap_arguments_if_possible(self, invocation: dict) -> list:
        command_invocation = InvocationWrapper().wrap(invocation)
        if self._is_fitting_in_line(command_invocation):
            return command_invocation['arguments']
        else:
            return invocation['arguments']

    @staticmethod
    def __remove_empty_arguments(invocation: dict) -> list:
        return list(filter(len, invocation['arguments']))

    @staticmethod
    def __remove_whitespace_at_end_of_line(args: List[str]) -> list:
        filtered_arguments = []
        for i in range(len(args) - 1):
            if not (Tokens.is_spacing_token(args[i]) and Tokens.is_spacing_token(args[i + 1])):
                filtered_arguments.append(args[i])
        return filtered_arguments + [args[-1]] if args else []
