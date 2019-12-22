import re


class FormatStartCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data: str) -> str:
        self.__state['indent'] += 1
        return self.__format_data(data)

    @staticmethod
    def __format_data(original: str) -> str:
        formatted = re.sub(r'\s+', '', original)
        return formatted.lower()
