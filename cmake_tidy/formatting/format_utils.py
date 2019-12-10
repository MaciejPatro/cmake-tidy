from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def exec(self, data) -> str:
        pass


class FormatNewline(Formatter):
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def exec(self, data) -> str:
        return self.__format_newlines(data) + self.__prepare_initial_newline_indent()

    def __prepare_initial_newline_indent(self) -> str:
        return self.__state['indent'] * self.__settings['tab_size'] * ' '

    def __format_newlines(self, number_of_newlines: int) -> str:
        return '\n' * min(self.__settings['succeeding_newlines'], number_of_newlines)


class FormatStartCommandInvocation(Formatter):
    def __init__(self, state: dict):
        self.__state = state

    def exec(self, data) -> str:
        if data.startswith('function'):
            self.__state['indent'] += 1
        elif data.startswith('endfunction'):
            self.__state['indent'] -= 1
        return data
