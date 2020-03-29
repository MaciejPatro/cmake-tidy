###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import sys
from pathlib import Path

from cmake_tidy.utils.app_configuration.configuration import Configuration, ConfigurationError


class FormatConfiguration(Configuration):
    def __init__(self, arguments: dict):
        super().__init__(arguments)
        self.__input_data = self.__initialize_input(arguments)
        self.__inplace = arguments['inplace']

    @property
    def input(self) -> str:
        return self.__input_data

    @property
    def inplace(self) -> str:
        return self._config.get(self._property_name()) is True

    @property
    def file(self) -> Path:
        return Path(self._config['input'])

    @property
    def command(self) -> str:
        return 'format'

    def __initialize_input(self, arguments) -> str:
        return self.__load_input_data(arguments)

    @staticmethod
    def __load_input_data(arguments) -> str:
        try:
            return Path(arguments['input']).read_text()
        except Exception:
            raise ConfigurationError('Error - incorrect \"input\" - please specify existing file to be formatted')
