from cmake_tidy.lex_data.elements import Element


class CMakeFormatter:
    __settings: dict

    def __init__(self, format_settings: dict):
        self.__settings = format_settings
        self.__state = {'indent': 0}

    def visit(self, name: str, values=None):
        if name in self.__format_methods:
            return self.__format_methods[name](values)

    def format(self, data: Element) -> str:
        formatted_elements = data.accept(self)
        return ''.join(formatted_elements)

    @property
    def __format_methods(self):
        formatting_methods = dict()

        formatting_methods['unhandled'] = \
            formatting_methods['file'] = \
            formatting_methods['line_comment'] = \
            formatting_methods['start_cmd_invoke'] = \
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
        formatting_methods['newlines'] = lambda lines: '\n' * min(self.__settings['succeeding_newlines'], lines)
        formatting_methods['line_ending'] = lambda data: ''.join(data)
        formatting_methods['quoted_argument'] = lambda data: f'"{data}"'
        return formatting_methods
