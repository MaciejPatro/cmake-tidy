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


class FormatLineEnding:
    def __init__(self):
        self.__callback = None

    def __call__(self, data: list) -> str:
        return self.__update_on_new_line(self.__format_line_ending(data))

    def on_line_end(self, callback) -> None:
        self.__callback = callback

    @staticmethod
    def __format_line_ending(data: list) -> str:
        return ''.join(data)

    def __update_on_new_line(self, formatted_line_ending: str) -> str:
        if self.__callback:
            return self.__callback(formatted_line_ending)
        return formatted_line_ending
