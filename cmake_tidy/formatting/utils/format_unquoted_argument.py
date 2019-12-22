class FormatUnquotedArgument:
    __keywords = ['TARGET']

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        self.__update_state(data)
        return data

    def __update_state(self, data: str) -> None:
        if self.__is_matching_any_of_keywords(data):
            self.__state['keyword_argument'] = True
            self.__state['indent'] += 1

    @staticmethod
    def __is_matching_any_of_keywords(data):
        return any([data == keyword for keyword in FormatUnquotedArgument.__keywords])
