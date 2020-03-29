###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


class _Executor:
    def __init__(self, state: dict, name: str, to_be_called):
        self.__state = state
        self.__name = name
        self.__to_be_called = to_be_called

    def __call__(self, arguments=None):
        if arguments is None:
            value = self.__to_be_called()
        else:
            value = self.__to_be_called(arguments)
        self.__state['last'] = self.__name
        return value


class CMakeFormatDispatcher:
    def __init__(self, state: dict):
        self.__state = state
        self.__dict = {}

    def __setitem__(self, key, value):
        if not callable(value):
            raise TypeError('Only callable values accepted')
        self.__dict[key] = _Executor(self.__state, key, value)

    def __getitem__(self, item):
        return self.__dict[item]

    def __contains__(self, item):
        return item in self.__dict
