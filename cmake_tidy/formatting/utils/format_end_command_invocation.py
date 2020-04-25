###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.tokens import Tokens


class FormatEndCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data: str) -> str:
        self.__update_state()
        return self.__format(data)

    def __update_state(self):
        if self.__state['keyword_argument']:
            self.__state['indent'] -= 1

    def __format(self, data):
        if self.__state['has_first_class_keyword']:
            return Tokens.reindent(3) + data
        if self.__state['keyword_argument']:
            return Tokens.reindent(2) + data
        return Tokens.reindent(1) + data
