###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.commands.format.format_configuration import FormatConfiguration
from cmake_tidy.commands.format.output_writer import OutputWriter


def try_create_configuration(arguments) -> FormatConfiguration:
    return FormatConfiguration(arguments=dict(vars(arguments)))
