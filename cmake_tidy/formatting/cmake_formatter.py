###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting import utils
from cmake_tidy.formatting.cmake_format_dispatcher import CMakeFormatDispatcher
from cmake_tidy.lexical_data.elements import Element
from cmake_tidy.utils.proxy_visitor import ProxyVisitor


class CMakeFormatter:
    __settings: dict

    def __init__(self, format_settings: dict):
        self.__state = {'indent': 0, 'last': None, 'keyword_argument': False, 'has_first_class_keyword': False}
        self.__settings = format_settings

        self.__formatters = CMakeFormatDispatcher(self.__state)
        self.__formatters['newlines'] = utils.FormatNewline(self.__state, self.__settings)
        self.__formatters['unquoted_argument'] = utils.FormatUnquotedArgument(self.__state, self.__settings)
        self.__formatters['start_cmd_invoke'] = utils.FormatStartCommandInvocation(self.__state, self.__settings)
        self.__formatters['command_invocation'] = utils.FormatCommandInvocation(self.__state, self.__settings)
        self.__formatters['file'] = utils.FormatFile(self.__settings)
        self.__formatters['spaces'] = utils.FormatSpaces(self.__settings, self.__state)
        self.__formatters['arguments'] = utils.FormatArguments(self.__state)
        self.__formatters['end_cmd_invoke'] = utils.FormatEndCommandInvocation(self.__state)
        self.__formatters['line_comment'] = lambda data: data
        self.__formatters['bracket_start'] = lambda data: data
        self.__formatters['bracket_end'] = lambda data: data
        self.__formatters['parenthesis_start'] = lambda data: data
        self.__formatters['parenthesis_end'] = lambda data: data
        self.__formatters['bracket_argument_content'] = lambda data: data
        self.__formatters['bracket_argument'] = lambda data: ''.join(data)
        self.__formatters['line_ending'] = lambda data: ''.join(data)
        self.__formatters['quoted_argument'] = lambda data: f'"{data}"'
        self.__formatters['parentheses'] = lambda data: data

    def format(self, data: Element) -> str:
        visitor = ProxyVisitor(self.__formatters)
        formatted_elements = data.accept(visitor)
        return ''.join(formatted_elements)
