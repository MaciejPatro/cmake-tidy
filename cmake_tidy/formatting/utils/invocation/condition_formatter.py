###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from typing import List

from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter
from cmake_tidy.formatting.utils.invocation.invocation_wrapper import InvocationWrapper
from cmake_tidy.formatting.utils.tokens import Tokens


class ConditionFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format(self, invocation: dict) -> str:
        invocation['arguments'] = self._prepare_arguments(invocation)
        invocation['arguments'] = self.__split_invocation_if_needed(invocation)
        return self._join_command_invocation(invocation)

    def __split_invocation_if_needed(self, invocation: dict) -> list:
        if not self._is_fitting_in_line(invocation):
            invocation = InvocationWrapper().wrap(invocation)
            return self.__split_invocation(invocation['arguments'])
        return invocation['arguments']

    def __split_invocation(self, args: List[str]) -> list:
        for i in range(len(args)):
            self.__update_state(args[i])
            self.__replace_token_with_newline_if_needed(args, i)
        return args

    def __replace_token_with_newline_if_needed(self, args: List[str], index: int):
        argument_diff = -1 if self._settings.get('condition_splitting_move_and_or_to_newline') else 1
        if (args[index] == 'OR' or args[index] == 'AND') and self.__is_spacing_token(args, index + argument_diff):
            args[index + argument_diff] = FormatNewline(self._state, self._settings)(1)

    def __update_state(self, token: str):
        if token == '(':
            self._state['indent'] += 1
        elif token == ')':
            self._state['indent'] -= 1

    @staticmethod
    def __is_spacing_token(args: List[str], index: int) -> bool:
        try:
            return Tokens.is_spacing_token(args[index])
        except IndexError:
            return False
