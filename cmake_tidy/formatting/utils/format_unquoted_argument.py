###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.updaters.keyword_state_updater import KeywordStateUpdater
from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.lexical_data import KeywordVerifier


class FormatUnquotedArgument:
    def __init__(self, state: dict, settings: dict):
        self.__verifier = KeywordVerifier(settings)
        self.__state_updater = KeywordStateUpdater(state, settings)
        self.__state = state
        self.__keyword_argument_already_found = False

    def __call__(self, data: str) -> str:
        self.__keyword_argument_already_found = self.__state['keyword_argument']
        self.__state_updater.update_state(data)
        return self.__format_data(data)

    def __format_data(self, data: str) -> str:
        if self.__keyword_argument_already_found and self.__is_reindent_needed(data):
            return Tokens.reindent(1) + data
        return data

    def __is_reindent_needed(self, data):
        return self.__verifier.is_keyword(data) or self.__verifier.is_property(data)
