import inspect


class Configuration:
    def __init__(self, arguments: dict):
        self._config = {}
        for name in self.__get_all_property_names():
            if arguments.get(name) is not None:
                self._config[name] = arguments.get(name)

    @property
    def input(self) -> str:
        input_file = self._config.get(self._property_name())
        if input_file is None:
            return ''
        else:
            return input_file.read()

    @property
    def all_properties(self):
        return {name: getattr(self, name) for name in self.__get_all_property_names()}

    @staticmethod
    def _property_name():
        return inspect.stack()[1][3]

    def __get_all_property_names(self) -> list:
        properties = [name for name, func in inspect.getmembers(self.__class__, self.__is_property)]
        properties.remove('all_properties')
        return properties

    @staticmethod
    def __is_property(v) -> bool:
        return isinstance(v, property)
