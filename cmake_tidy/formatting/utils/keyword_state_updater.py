###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.utils.keyword_verifier import KeywordVerifier


class KeywordStateUpdater:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__verifier = KeywordVerifier(settings)

    def update_state(self, argument: str) -> None:
        if self.__verifier.is_first_class_keyword(argument):
            self.__state['has_first_class_keyword'] = True
            self.__state['indent'] += 1
        elif self.__verifier.is_keyword(argument):
            if not self.__state['keyword_argument']:
                self.__state['indent'] += 1
            self.__state['keyword_argument'] = True
