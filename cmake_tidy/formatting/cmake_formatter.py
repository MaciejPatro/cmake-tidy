from cmake_tidy.formatting.format_utils import FormatNewline, FormatStartCommandInvocation, FormatFile
from cmake_tidy.lex_data.elements import Element
from cmake_tidy.utils.proxy_visitor import ProxyVisitor


class CMakeFormatter:
    __settings: dict

    def __init__(self, format_settings: dict):
        self.__state = {'indent': 0}
        self.__settings = format_settings

        self.__formatters = {'newlines': FormatNewline(self.__state, self.__settings),
                             'start_cmd_invoke': FormatStartCommandInvocation(self.__state),
                             'file': FormatFile(self.__settings),
                             'unhandled': lambda data: data,
                             'line_comment': lambda data: data,
                             'end_cmd_invoke': lambda data: data,
                             'arguments': lambda data: ''.join(data),
                             'bracket_start': lambda data: data,
                             'bracket_end': lambda data: data,
                             'unquoted_argument': lambda data: data,
                             'bracket_argument_content': lambda data: data,
                             'file_element': lambda data: ''.join(data),
                             'command_invocation': lambda data: ''.join(data),
                             'bracket_argument': lambda data: ''.join(data),
                             'spaces': lambda data: data.replace('\t', ' ' * self.__settings['tab_size']),
                             'line_ending': lambda data: ''.join(data),
                             'quoted_argument': lambda data: f'"{data}"'}

    def format(self, data: Element) -> str:
        visitor = ProxyVisitor(self.__formatters)
        formatted_elements = data.accept(visitor)
        return ''.join(formatted_elements)
