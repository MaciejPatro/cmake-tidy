###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter
from cmake_tidy.formatting.utils.invocation.invocation_wrapper import InvocationWrapper
from cmake_tidy.formatting.utils.invocation.utils import fix_line_comments


class ConditionFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format(self, invocation: dict) -> str:
        invocation['arguments'] = self._prepare_arguments(invocation)
        invocation['arguments'] = self.__split_invocation_if_needed(invocation)
        invocation['arguments'] = fix_line_comments(invocation['arguments'])
        return self._join_command_invocation(invocation)

    def __split_invocation_if_needed(self, invocation: dict) -> list:
        if not self._is_fitting_in_line(invocation):
            invocation = InvocationWrapper().wrap(invocation)
            return self.__split_invocation(invocation['arguments'])
        return invocation['arguments']

    def __split_invocation(self, args: List[str]) -> list:
        for i in range(1, len(args) - 1):
            if (args[i] == 'OR' or args[i] == 'AND') and args[i + 1] == ' ':
                args[i + 1] = FormatNewline(self._state, self._settings)(1)
        return args
