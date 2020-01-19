from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.utils.keyword_verifier import KeywordVerifier


class FormatUnquotedArgument:
    def __init__(self, state: dict, settings: dict):
        self.__verifier = KeywordVerifier(settings)
        self.__state = state
        self.__keyword_argument_already_found = False

    def __call__(self, data) -> str:
        self.__keyword_argument_already_found = self.__state['keyword_argument']
        self.__update_state(data)
        return self.__format_data(data)

    def __update_state(self, data: str) -> None:
        if self.__verifier.is_keyword(data):
            if not self.__state['keyword_argument']:
                self.__state['indent'] += 1
            self.__state['keyword_argument'] = True

    def __format_data(self, data: str) -> str:
        if self.__keyword_argument_already_found:
            return Tokens.reindent + data
        return data