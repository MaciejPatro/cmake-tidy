from cmake_tidy.formatting.utils.tokens import Tokens


class FormatFile:
    def __init__(self, settings: dict):
        self.__settings = settings

    def __call__(self, data) -> str:
        return self.__cleanup_end_invocations(''.join(data))

    def __cleanup_end_invocations(self, formatted_file: str) -> str:
        indent = self.__settings['tab_size'] * ' '
        formatted_file = formatted_file.replace(2 * indent + Tokens.reindent_2, '')
        formatted_file = formatted_file.replace(indent + Tokens.reindent, '')
        formatted_file = formatted_file.replace(Tokens.reindent, '')
        return formatted_file
