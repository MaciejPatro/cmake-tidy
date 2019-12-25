from pathlib import Path

from cmake_tidy.utils.app_configuration.configuration import Configuration, ConfigurationError


class FormatConfiguration(Configuration):
    def __init__(self, arguments: dict):
        super().__init__(arguments)
        self.__input_data = self.__load_input_data(arguments)

    @property
    def input(self) -> str:
        return self.__input_data

    @staticmethod
    def __load_input_data(arguments) -> str:
        try:
            return Path(arguments['input']).read_text()
        except Exception:
            raise ConfigurationError('Error - incorrect \"input\" - please specify existing file to be formatted')
