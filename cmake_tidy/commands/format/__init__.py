from cmake_tidy.commands.format.format_configuration import FormatConfiguration


def try_create_configuration(arguments):
    return FormatConfiguration(arguments=dict(vars(arguments)))
