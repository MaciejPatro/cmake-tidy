###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.command_formatter import CommandFormatter
from cmake_tidy.formatting.utils.updaters.command_invocatin_state_updater import CommandInvocationStateUpdater


class FormatCommandInvocation:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__state_handler = CommandInvocationStateUpdater(state)
        self.__settings = settings

    def __call__(self, data: list) -> str:
        command_invocation = self.__prepare_data(data)
        formatted = self.__format_invocation(command_invocation)
        self.__state_handler.update_state(command_invocation['function_name'])
        return formatted

    @staticmethod
    def __prepare_data(data: list) -> dict:
        return {'function_name': data[0],
                'arguments': data[1] if len(data) == 3 else [],
                'closing': data[2] if len(data) == 3 else data[1]}

    def __format_invocation(self, invocation: dict) -> str:
        return CommandFormatter(self.__state, self.__settings).format_invocation(invocation)
