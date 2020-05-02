###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter
from cmake_tidy.formatting.utils.invocation.command_splitter import CommandSplitter


class CommandFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format(self, invocation: dict) -> str:
        invocation['arguments'] = self._prepare_arguments(invocation)
        if not self._is_fitting_in_line(invocation):
            invocation['arguments'] = self.__split_command_to_newlines(invocation)
        return self._join_command_invocation(invocation)

    def __split_command_to_newlines(self, invocation: dict) -> list:
        return CommandSplitter(self._state, self._settings).split(invocation)
