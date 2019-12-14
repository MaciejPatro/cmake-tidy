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

    def __call__(self, data) -> str:
        if data.startswith('function'):
            self.__state['indent'] += 1
        elif data.startswith('endfunction'):
            self.__state['indent'] -= 1
        return data


class FormatFile:
    def __init__(self, settings: dict):
        self.__settings = settings

    def __call__(self, data) -> str:
        return self.__cleanup_end_invocations(''.join(data))

    def __cleanup_end_invocations(self, formatted_file: str) -> str:
        indent = self.__settings['tab_size'] * ' '
        return formatted_file.replace(indent + 'endfunction', 'endfunction')
