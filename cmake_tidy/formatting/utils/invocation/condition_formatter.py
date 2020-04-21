###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter


class ConditionFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format(self, invocation: dict) -> str:
        invocation['arguments'] = self._prepare_arguments(invocation)
        invocation['arguments'] = self.__split_invocation_if_needed(invocation)
        return self._join_command_invocation(invocation)

    def __split_invocation_if_needed(self, invocation: dict) -> list:
        if not self._is_fitting_in_line(invocation):
            return self.__split_invocation(invocation['arguments'])
        return invocation['arguments']

    def __split_invocation(self, args: List[str]) -> list:
        self.__increment_indent()
        args = self.__split_arguments_after_logical_operands(args)
        self.__rollback_indent()
        return args

    def __split_arguments_after_logical_operands(self, args: List[str]) -> list:
        for i in range(1, len(args) - 1):
            if args[i] == 'OR' or args[i] == 'AND':
                args[i + 1] = FormatNewline(self._state, self._settings)(1)
        return args

    def __increment_indent(self):
        self._state['indent'] += 1

    def __rollback_indent(self):
        self._state['indent'] -= 1
