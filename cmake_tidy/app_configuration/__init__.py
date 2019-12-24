from cmake_tidy.app_configuration.format_configuration import FormatConfiguration


def create_configuration(arguments):
    return FormatConfiguration(arguments=dict(vars(arguments)))
