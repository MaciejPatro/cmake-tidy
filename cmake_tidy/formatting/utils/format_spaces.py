class FormatSpaces:
    def __init__(self, settings: dict, state: dict):
        self.__settings = settings
        self.__state = state

    def __call__(self, data) -> str:
        if self.__state['last'] is 'line_ending':
            return ''
        return data.replace('\t', ' ' * self.__settings['tab_size'])
