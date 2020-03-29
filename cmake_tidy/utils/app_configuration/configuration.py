###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import inspect


class ConfigurationError(Exception):
    pass


class Configuration:
    def __init__(self, arguments):
        self._config = {}
        for name in self.__get_all_property_names():
            if arguments.get(name) is not None:
                self._config[name] = arguments.get(name)

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
