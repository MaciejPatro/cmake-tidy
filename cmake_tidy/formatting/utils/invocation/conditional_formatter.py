###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter


class ConditionalFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format(self, invocation: dict) -> str:
        return self._join_command_invocation(invocation)
