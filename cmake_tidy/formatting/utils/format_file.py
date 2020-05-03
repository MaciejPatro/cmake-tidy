###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re

from cmake_tidy.formatting.utils.single_indent import get_single_indent
from cmake_tidy.formatting.utils.tokens import Tokens


class FormatFile:
    def __init__(self, settings: dict):
        self.__settings = settings

    def __call__(self, data: list) -> str:
        processed = self.__cleanup_end_invocations(''.join(data))
        return self.__cleanup_whitespaces_at_line_ends(processed)

    def __cleanup_end_invocations(self, formatted_file: str) -> str:
        for pattern in Tokens.get_reindent_patterns_list(3, get_single_indent(self.__settings)):
            formatted_file = re.sub(pattern, '', formatted_file)
        return formatted_file

    @staticmethod
    def __cleanup_whitespaces_at_line_ends(processed: str) -> str:
        return re.sub('[ \t]*' + Tokens.remove_spaces(), '', processed)
