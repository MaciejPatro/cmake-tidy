###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.invocation_splitter import InvocationSplitter
from cmake_tidy.formatting.utils.invocation.invocation_wrapper import InvocationWrapper
from cmake_tidy.formatting.utils.single_indent import get_single_indent
from cmake_tidy.formatting.utils.tokens import Tokens


class InvocationFormatter:
    def __init__(self, state: dict, settings: dict):
        self._settings = settings
        self._state = state

    @staticmethod
    def _remove_empty_arguments(invocation: dict) -> list:
        return list(filter(len, invocation['arguments']))

    def _is_wrappable(self, invocation: dict) -> bool:
        return len(invocation['arguments']) > 0 and self._settings['wrap_short_invocations_to_single_line'] is True

    def _wrap_arguments_if_possible(self, invocation: dict) -> list:
        command_invocation = InvocationWrapper().wrap(invocation)
        if self._is_fitting_in_line(command_invocation):
            return command_invocation['arguments']
        else:
            return invocation['arguments']

    def _is_fitting_in_line(self, command_invocation: dict) -> bool:
        return self._invocation_length(command_invocation) < self._settings['line_length']

    def _newline_indent(self) -> str:
        indent = max(self._state['indent'] - 1, 0)
        return indent * get_single_indent(self._settings)

    def _invocation_length(self, command_invocation: dict) -> int:
        invoke = self._join_command_invocation(command_invocation) + self._newline_indent()
        invoke = invoke.replace('\t', ' ' * self._settings['tab_size'])
        return len(invoke) - len(Tokens.reindent(1))

    @staticmethod
    def _join_command_invocation(invocation: dict) -> str:
        formatted = invocation['function_name'] + ''.join(invocation['arguments']) + invocation['closing']
        return formatted


class CommandFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format_invocation(self, invocation: dict) -> str:
        invocation['arguments'] = self.__prepare_arguments(invocation)
        formatted = self._join_command_invocation(invocation)
        return self.__add_reindent_tokens_where_needed(formatted)

    def __prepare_arguments(self, invocation: dict) -> list:
        invocation['arguments'] = self._remove_empty_arguments(invocation)
        if self._is_wrappable(invocation):
            invocation['arguments'] = self._wrap_arguments_if_possible(invocation)
        if not self._is_fitting_in_line(invocation):
            invocation['arguments'] = self.__split_command_to_newlines(invocation)
        return invocation['arguments']

    def __split_command_to_newlines(self, invocation: dict) -> list:
        return InvocationSplitter(self._state, self._settings).split(invocation)

    @staticmethod
    def __add_reindent_tokens_where_needed(data: str) -> str:
        data_lower = data.lower()
        if any(data_lower.startswith(token) for token in Tokens.reindent_commands_tokens()):
            return Tokens.reindent(1) + data
        return data
