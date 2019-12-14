class CMakeFormatDispatcher:
    def __init__(self, state: dict):
        self.__state = state
        self.__dict = {}

    def __setitem__(self, key, value):
        self.__dict[key] = value
