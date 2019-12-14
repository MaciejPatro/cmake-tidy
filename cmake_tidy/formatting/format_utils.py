class FormatNewline:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data) -> str:
        return self.__format_newlines(data) + self.__prepare_initial_newline_indent()

    def __prepare_initial_newline_indent(self) -> str:
        return self.__state['indent'] * self.__settings['tab_size'] * ' '

    def __format_newlines(self, number_of_newlines: int) -> str:
        return '\n' * min(self.__settings['succeeding_newlines'], number_of_newlines)


class FormatStartCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state
        self.__invocations_with_indent = ['function', 'if']

    def __call__(self, data) -> str:
        self.__update_indent(data)
        return data

    def __update_indent(self, data: str) -> None:
        if data.startswith(self.__start_indents()):
            self.__state['indent'] += 1
        elif data.startswith(self.__end_indents()):
            self.__state['indent'] -= 1

    def __start_indents(self) -> tuple:
        return tuple(self.__invocations_with_indent)

    def __end_indents(self) -> tuple:
        return tuple(f'end{x}' for x in self.__invocations_with_indent)


class FormatFile:
    def __init__(self, settings: dict):
        self.__settings = settings
        self.__elements_to_ident_backward = ['endfunction', 'endif']

    def __call__(self, data) -> str:
        return self.__cleanup_end_invocations(''.join(data))

    def __cleanup_end_invocations(self, formatted_file: str) -> str:
        indent = self.__settings['tab_size'] * ' '
        for element in self.__elements_to_ident_backward:
            formatted_file = formatted_file.replace(indent + element, element)
        return formatted_file


class FormatSpaces:
    def __init__(self, settings: dict):
        self.__settings = settings

    def __call__(self, data) -> str:
        return data.replace('\t', ' ' * self.__settings['tab_size'])
