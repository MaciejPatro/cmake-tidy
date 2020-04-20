###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################
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
