from cmake_tidy.parsing.elements import Element
from cmake_tidy.utils.proxy_visitor import ProxyVisitor


class CMakeFormatter:
    def __init__(self):
        self.__visitor = ProxyVisitor(self.__generate_formatting_methods())

    def format(self, data: Element) -> str:
        formatted_elements = data.accept(self.__visitor)
        return ''.join(formatted_elements)

    @staticmethod
    def __generate_formatting_methods():
        formatting_methods = dict()
        formatting_methods['unhandled'] = lambda data: data
        formatting_methods['file'] = lambda data: data
        formatting_methods['line_comment'] = lambda data: data
        formatting_methods['line_ending'] = lambda data: ''.join(data)
        formatting_methods['newlines'] = lambda newlines: '\n' * min(2, newlines)
        return formatting_methods
