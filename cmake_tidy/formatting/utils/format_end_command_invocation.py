from cmake_tidy.formatting.utils.tokens import Tokens


class FormatEndCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data: str) -> str:
        if self.__state['keyword_argument']:
            return Tokens.reindent_2 + data
        return Tokens.reindent + data
