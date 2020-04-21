###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.format_newline import FormatNewline
from cmake_tidy.formatting.utils.invocation.invocation_formatter import InvocationFormatter


class ConditionalFormatter(InvocationFormatter):
    def __init__(self, state: dict, settings: dict):
        super().__init__(state, settings)

    def format(self, invocation: dict) -> str:
        invocation['arguments'] = self._prepare_arguments(invocation)
        if not self._is_fitting_in_line(invocation):
            self._state['indent'] += 1
            args = invocation['arguments']
            for i in range(1, len(args) - 1):
                if args[i] == 'OR' or args[i] == 'AND':
                    args[i + 1] = FormatNewline(self._state, self._settings)(1)
            self._state['indent'] -= 1
        return self._join_command_invocation(invocation)
