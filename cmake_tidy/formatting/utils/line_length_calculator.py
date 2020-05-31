###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re

from cmake_tidy.formatting.utils.tokens import Tokens


class LineLengthCalculator:
    def __init__(self, settings: dict):
        self.__settings = settings

    def calculate(self, invocation: str) -> int:
        invocation = invocation.replace('\t', ' ' * self.__settings['tab_size'])
        invocation = re.sub(Tokens.get_reindent_regex(), '', invocation)
        invocation = re.sub(Tokens.remove_spaces(), '', invocation)
        return len(invocation)
