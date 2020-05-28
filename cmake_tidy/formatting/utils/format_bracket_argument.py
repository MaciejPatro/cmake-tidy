###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.formatting.utils.tokens import Tokens


class FormatBracketArgument:
    def __call__(self, data: list) -> str:
        formatted = ''.join(data)
        if '\n' in data[1]:
            formatted = Tokens.reindent(99) + formatted
        return formatted
