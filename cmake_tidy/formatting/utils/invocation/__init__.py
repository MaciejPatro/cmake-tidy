###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.invocation.command_formatter import CommandFormatter
from cmake_tidy.formatting.utils.invocation.condition_formatter import ConditionFormatter
from cmake_tidy.lexical_data import KeywordVerifier


def format_command_invocation(state: dict, settings: dict, invocation: dict) -> str:
    if KeywordVerifier.is_conditional_invocation(invocation['function_name']):
        return ConditionFormatter(state, settings).format(invocation)
    return CommandFormatter(state, settings).format(invocation)
