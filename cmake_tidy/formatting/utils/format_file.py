from cmake_tidy.formatting.utils.single_indent import get_single_indent
from cmake_tidy.formatting.utils.tokens import Tokens


class FormatFile:
    def __init__(self, settings: dict):
        self.__settings = settings

    def __call__(self, data: list) -> str:
        return self.__cleanup_end_invocations(''.join(data))

    def __cleanup_end_invocations(self, formatted_file: str) -> str:
        indent = get_single_indent(self.__settings)
        for pattern in [2 * indent + Tokens.reindent_2,
                        indent + Tokens.reindent_2,
                        indent + Tokens.reindent,
                        Tokens.reindent_2,
                        Tokens.reindent]:
            formatted_file = formatted_file.replace(pattern, '')
        return formatted_file
