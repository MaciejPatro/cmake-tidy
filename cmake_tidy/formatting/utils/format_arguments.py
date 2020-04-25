###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re
from iteration_utilities import deepflatten


class FormatArguments:
    __spacing = r'^[ \t]+$'

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data: list) -> list:
        return self.__format_arguments(data) if data[0] else []

    def __format_arguments(self, data: list) -> list:
        data = list(deepflatten(data, types=list))
        data = self.__replace_spacings_between_arguments_with_single_space(data)
        data = self.__remove_spacing_from_first_element(data)
        data = self.__remove_spacing_from_last_element(data)
        return data

    @staticmethod
    def __replace_spacings_between_arguments_with_single_space(data: list) -> list:
        return [re.sub(FormatArguments.__spacing, ' ', element) for element in data]

    @staticmethod
    def __remove_spacing_from_first_element(data: list) -> list:
        return data[1:] if re.match(FormatArguments.__spacing, data[0]) else data

    @staticmethod
    def __remove_spacing_from_last_element(data: list) -> list:
        return data[:-1] if re.match(FormatArguments.__spacing, data[-1]) else data
