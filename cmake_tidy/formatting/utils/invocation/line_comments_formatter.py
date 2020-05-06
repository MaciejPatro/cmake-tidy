###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re
from typing import List

from cmake_tidy.formatting.utils.tokens import Tokens
from cmake_tidy.lexical_data import KeywordVerifier


class LineCommentsFormatter:
    def __init__(self, settings: dict):
        self.__settings = settings

    def format(self, args: List[str]) -> list:
        args = self.__reindent_line_comments(args)
        return self.__merge_line_comments_with_whitespaces_before(args)

    @staticmethod
    def __merge_line_comments_with_whitespaces_before(args: List[str]) -> list:
        merged = []
        for i in range(len(args) - 1):
            if Tokens.is_spacing_token(args[i]) and Tokens.is_line_comment(args[i + 1]):
                args[i + 1] = args[i] + args[i + 1]
            else:
                merged.append(args[i])
        return merged + [args[-1]] if args else []

    def __reindent_line_comments(self, args: List[str]) -> list:
        verifier = KeywordVerifier(self.__settings)

        for i in reversed(range(len(args))):
            if verifier.is_keyword(args[i]) and re.match(Tokens.get_reindent_regex(), args[i]):
                self.__try_reindent_all_comments_after_keyword(args, i)
        return args

    def __try_reindent_all_comments_after_keyword(self, args, i):
        try:
            self.__reindent_all_comments_after_keyword(args, i)
        except IndexError:
            pass

    @staticmethod
    def __reindent_all_comments_after_keyword(args: list, start: int) -> None:
        for i in reversed(range(start)):
            if Tokens.is_line_comment(args[i]):
                args[i] = Tokens.reindent(1) + args[i]
            else:
                break
