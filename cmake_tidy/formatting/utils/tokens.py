###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


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
    def get_reindent_patterns_list(count: int, indent: str) -> list:
        return [f'({indent}){{0,{times}}}{Tokens.reindent(times)}' for times in range(1, count + 1)]
