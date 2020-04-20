###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter
from cmake_tidy.formatting.utils.invocation.invocation_splitter import InvocationSplitter


class CommandFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format(self, invocation: dict) -> str:
        invocation['arguments'] = self.__prepare_arguments(invocation)
        return self._join_command_invocation(invocation)

    def __prepare_arguments(self, invocation: dict) -> list:
        invocation['arguments'] = self._remove_empty_arguments(invocation)
        if self._is_wrappable(invocation):
            invocation['arguments'] = self._wrap_arguments_if_possible(invocation)
        if not self._is_fitting_in_line(invocation):
            invocation['arguments'] = self.__split_command_to_newlines(invocation)
        return invocation['arguments']

    def __split_command_to_newlines(self, invocation: dict) -> list:
        return InvocationSplitter(self._state, self._settings).split(invocation)

