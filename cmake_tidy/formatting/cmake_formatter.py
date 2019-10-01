from cmake_tidy.parsing.elements import Element
from cmake_tidy.utils.proxy_visitor import ProxyVisitor


class CMakeFormatter:
    def __init__(self, format_settings: dict):
        self.__settings = format_settings
        self.__visitor = ProxyVisitor(self.__generate_formatting_methods())

    def format(self, data: Element) -> str:
        formatted_elements = data.accept(self.__visitor)
        return ''.join(formatted_elements)

    def __generate_formatting_methods(self):
        formatting_methods = dict()
        formatting_methods['unhandled'] = lambda data: data
        formatting_methods['file'] = lambda data: data
        formatting_methods['line_comment'] = lambda data: data
        formatting_methods['line_ending'] = lambda data: ''.join(data)
        formatting_methods['newlines'] = lambda newlines: '\n' * min(self.__settings['succeeding_newlines'], newlines)
        return formatting_methods
