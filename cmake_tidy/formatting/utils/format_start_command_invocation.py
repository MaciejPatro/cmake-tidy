import re


class FormatStartCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data: str) -> str:
        self.__state['indent'] += 1
        return re.sub(r'\s+', '', data)
