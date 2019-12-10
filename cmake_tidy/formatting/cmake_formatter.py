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
                             'file': FormatFile(self.__settings)}

    def format(self, data: Element) -> str:
        visitor = ProxyVisitor(self.__format_methods())
        formatted_elements = data.accept(visitor)
        return ''.join(formatted_elements)

    def __format_methods(self):
        formatting_methods = dict()

        formatting_methods['unhandled'] = \
            formatting_methods['line_comment'] = \
            formatting_methods['end_cmd_invoke'] = \
            formatting_methods['arguments'] = \
            formatting_methods['bracket_start'] = \
            formatting_methods['bracket_end'] = \
            formatting_methods['unquoted_argument'] = \
            formatting_methods['bracket_argument_content'] = lambda data: data

        formatting_methods['file_element'] = \
            formatting_methods['command_invocation'] = \
            formatting_methods['bracket_argument'] = \
            formatting_methods['arguments'] = lambda data: ''.join(data)

        formatting_methods['spaces'] = lambda data: data.replace('\t', ' ' * self.__settings['tab_size'])
        formatting_methods['line_ending'] = lambda data: ''.join(data)
        formatting_methods['quoted_argument'] = lambda data: f'"{data}"'

        formatting_methods['file'] = self.__formatters['file'].exec
        formatting_methods['start_cmd_invoke'] = self.__formatters['start_cmd_invoke'].exec
        formatting_methods['newlines'] = self.__formatters['newlines'].exec

        return formatting_methods
