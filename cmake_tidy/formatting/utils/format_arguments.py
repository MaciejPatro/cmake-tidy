import re


class FormatArguments:
    __spacing = r'^[ \t]+$'

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        if data[0]:
            self.__update_state()
            return self.__format_arguments(data)
        return ''

    def __update_state(self):
        if self.__state['keyword_argument']:
            self.__state['indent'] -= 1

    def __format_arguments(self, data) -> str:
        data = self.__replace_spacings_between_arguments_with_single_space(data)
        data = self.__remove_spacing_from_first_element(data)
        data = self.__remove_spacing_from_last_element(data)
        return ''.join(data)

    @staticmethod
    def __replace_spacings_between_arguments_with_single_space(data: list) -> list:
        return [re.sub(FormatArguments.__spacing, ' ', element) for element in data]

    @staticmethod
    def __remove_spacing_from_first_element(data: list) -> list:
        return data[1:] if re.match(FormatArguments.__spacing, data[0]) else data

    @staticmethod
    def __remove_spacing_from_last_element(data: list) -> list:
        return data[:-1] if re.match(FormatArguments.__spacing, data[-1]) else data
