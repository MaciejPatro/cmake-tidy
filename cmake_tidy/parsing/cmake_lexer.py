import ply.lex as lex


class CMakeLexer:
    tokens = ['NEWLINES']

    def __init__(self) -> None:
        self.lexer = lex.lex(module=self)

    @staticmethod
    def t_NEWLINES(t: lex.LexToken) -> lex.LexToken:
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        return t

    @staticmethod
    def t_ANY_error(t: lex.LexToken) -> None:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def analyze(self, data: str) -> list:
        self.lexer.input(data)
        data = []

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            data.append(tok)

        return data
