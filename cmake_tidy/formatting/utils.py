class FormatNewlines:
    def __init__(self, settings: dict):
        self.__succeeding_newlines = settings['succeeding_newlines']

    def __call__(self, num_of_newlines: int) -> str:
        return '\n' * min(self.__succeeding_newlines, num_of_newlines)


class FormatSpaces:
    def __init__(self, settings: dict):
        self.__tab_size = settings['tab_size']

    def __call__(self, data: str) -> str:
        return data.replace('\t', ' ' * self.__tab_size)
