from cmake_tidy.utils.configuration import Configuration


class FormatConfiguration(Configuration):
    def __init__(self, arguments: dict):
        super().__init__(arguments)
        self.__input_data = None

    @property
    def input(self) -> str:
        input_file = self._config.get(self._property_name())
        if input_file is None:
            return ''
        return self.__get_input_data_from_file(input_file)

    def __get_input_data_from_file(self, input_file):
        if self.__input_data is None:
            self.__input_data = input_file.read()
            input_file.close()
        return self.__input_data
