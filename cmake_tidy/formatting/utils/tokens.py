###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import re


class Tokens:
    @staticmethod
    def start_tokens() -> list:
        return ['macro', 'while', 'foreach', 'if', 'function']

    @staticmethod
    def end_tokens() -> list:
        return [f'end{token}' for token in Tokens.start_tokens()]

    @staticmethod
    def reindent_commands_tokens() -> list:
        return ['elseif', 'else'] + Tokens.end_tokens()

    @staticmethod
    def conditional_tokens() -> list:
        return ['if', 'while', 'foreach', 'elseif']

    @staticmethod
    def reindent(count: int) -> str:
        return f'<cmake-tidy-reindent{count}>'

    @staticmethod
    def remove_spaces() -> str:
        return '<cmake-tidy-remove-space>'

    @staticmethod
    def is_spacing_token(data: str) -> bool:
        data = data.replace(Tokens.remove_spaces(), '')
        return re.match(r'^\s+$', data) is not None

    @staticmethod
    def get_reindent_regex() -> str:
        return r'<cmake-tidy-reindent[0-9]+>'

    @staticmethod
    def get_reindent_patterns_list(count: int, indent: str) -> list:
        return [f'({indent}){{0,{times}}}{Tokens.reindent(times)}' for times in range(1, count + 1)]

    @staticmethod
    def is_line_comment(data: str) -> bool:
        data = re.sub(Tokens.get_reindent_regex(), '', data)
        data = re.sub(Tokens.remove_spaces(), '', data)
        return data.strip().startswith('#')
