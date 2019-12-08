from cmake_tidy.app_configuration.configuration import Configuration


def create_configuration(arguments):
    return Configuration(arguments=dict(vars(arguments)))
