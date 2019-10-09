import ply.lex as lex


class CMakeLexer:
    tokens = ['NEWLINES', 'UNHANDLED_YET', 'LINE_COMMENT', 'SPACES']

    t_LINE_COMMENT = r'\#[^\n]+'
    t_SPACES = r'[ \t]+'

    def __init__(self) -> None:
        self.lexer = lex.lex(module=self)

    @staticmethod
    def t_NEWLINES(t: lex.LexToken) -> lex.LexToken:
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        return t

    @staticmethod
    def t_ANY_error(t: lex.LexToken) -> None:
        print(f'Unsupported: {t.value[0]}')
        t.lexer.skip(1)

    @staticmethod
    def t_UNHANDLED_YET(t: lex.Token) -> lex.Token:
        r"""[\w\d\.\"\-\=\$\{\}\/\)\(\<\:\>]+"""
        return t

    def analyze(self, data: str) -> list:
        self.lexer.input(data)
        data = []

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            data.append(tok)

        return data
