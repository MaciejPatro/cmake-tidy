from cmake_tidy.formatting.cmake_format_dispatcher import CMakeFormatDispatcher
from cmake_tidy.formatting.format_utils import FormatNewline, FormatStartCommandInvocation, FormatFile, FormatSpaces, \
    FormatArguments, FormatCommandInvocation
from cmake_tidy.lex_data.elements import Element
from cmake_tidy.utils.proxy_visitor import ProxyVisitor


class CMakeFormatter:
    __settings: dict

    def __init__(self, format_settings: dict):
        self.__state = {'indent': 0, 'last': None}
        self.__settings = format_settings

        self.__formatters = CMakeFormatDispatcher(self.__state)
        self.__formatters['newlines'] = FormatNewline(self.__state, self.__settings)
        self.__formatters['start_cmd_invoke'] = FormatStartCommandInvocation(self.__state)
        self.__formatters['file'] = FormatFile(self.__settings)
        self.__formatters['spaces'] = FormatSpaces(self.__settings, self.__state)
        self.__formatters['command_invocation'] = FormatCommandInvocation(self.__state)
        self.__formatters['arguments'] = FormatArguments()
        self.__formatters['unhandled'] = lambda data: data
        self.__formatters['line_comment'] = lambda data: data
        self.__formatters['end_cmd_invoke'] = lambda data: data
        self.__formatters['bracket_start'] = lambda data: data
        self.__formatters['bracket_end'] = lambda data: data
        self.__formatters['unquoted_argument'] = lambda data: data
        self.__formatters['bracket_argument_content'] = lambda data: data
        self.__formatters['bracket_argument'] = lambda data: ''.join(data)
        self.__formatters['line_ending'] = lambda data: ''.join(data)
        self.__formatters['quoted_argument'] = lambda data: f'"{data}"'

    def format(self, data: Element) -> str:
        visitor = ProxyVisitor(self.__formatters)
        formatted_elements = data.accept(visitor)
        return ''.join(formatted_elements)
