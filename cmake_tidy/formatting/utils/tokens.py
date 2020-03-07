class Tokens:
    @staticmethod
    def reindent(count: int) -> str:
        return f'<cmake-tidy-reindent{count}>'

    @staticmethod
    def get_reindent_patterns_list(count: int, indent: str) -> list:
        return [f'({indent}){{0,{times}}}{Tokens.reindent(times)}' for times in range(1, count + 1)]
