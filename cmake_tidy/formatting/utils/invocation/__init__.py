###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.command_formatter import CommandFormatter
from cmake_tidy.formatting.utils.invocation.conditional_formatter import ConditionalFormatter
from cmake_tidy.lexical_data import KeywordVerifier


def format_command_invocation(state: dict, settings: dict, invocation: dict) -> str:
    if KeywordVerifier.is_conditional_invocation(invocation['function_name']):
        return ConditionalFormatter(state, settings).format(invocation)
    return CommandFormatter(state, settings).format(invocation)
