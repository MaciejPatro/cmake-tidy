import re


class FormatStartCommandInvocation:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data: str) -> str:
        self.__state['indent'] += 1
        return self.__format_data(data)

    def __format_data(self, original: str) -> str:
        formatted = self.__remove_whitespaces_after_name(original)
        return self.__unify_command_name(formatted)

    def __unify_command_name(self, formatted):
        if self.__settings.get('force_command_lowercase'):
            return formatted.lower()
        return formatted

    @staticmethod
    def __remove_whitespaces_after_name(original):
        formatted = re.sub(r'\s+', '', original)
        return formatted
