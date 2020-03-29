###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.single_indent import get_single_indent


class FormatSpaces:
    def __init__(self, settings: dict, state: dict):
        self.__settings = settings
        self.__state = state

    def __call__(self, data: str) -> str:
        if self.__state['last'] == 'line_ending':
            return ''
        elif self.__state['last'] == 'command_invocation':
            return ' '
        return data.replace('\t', get_single_indent(self.__settings))
