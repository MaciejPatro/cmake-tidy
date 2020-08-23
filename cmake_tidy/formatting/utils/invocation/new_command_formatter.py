###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


class NewCommandFormatter:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    @staticmethod
    def format(invocation: dict) -> str:
        return invocation['function_name'] + ''.join(invocation['arguments']) + invocation['closing']
