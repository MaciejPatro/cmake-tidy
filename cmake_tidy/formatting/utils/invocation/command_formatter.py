###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################
from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter
from cmake_tidy.formatting.utils.invocation.invocation_splitter import InvocationSplitter
from cmake_tidy.formatting.utils.tokens import Tokens


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
