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
    def t_ANY_error(t: lex.LexToken):
        t.lexer.skip(1)
        t.type = 'UNHANDLED_YET'
        t.value = t.value[0]
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
