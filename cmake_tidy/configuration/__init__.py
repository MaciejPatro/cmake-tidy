from cmake_tidy.configuration.configuration import Configuration


def create_configuration(arguments):
    return Configuration(arguments=dict(vars(arguments)))
