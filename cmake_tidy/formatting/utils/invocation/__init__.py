###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.command_formatter import CommandFormatter


def format_command_invocation(state: dict, settings: dict, invocation: dict) -> str:
    return CommandFormatter(state, settings).format(invocation)
