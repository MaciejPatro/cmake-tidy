class CMakeFormatDispatcher:
    def __init__(self, state: dict):
        self.__state = state
        self.__dict = {}

    def __setitem__(self, key, value):
        if not callable(value):
            raise TypeError('Only callable values accepted')
        self.__dict[key] = value

    def __getitem__(self, item):
        return self.__exec(item)

    def __exec(self, item):
        value = self.__dict[item]()
        self.__state['last'] = item
        return value
