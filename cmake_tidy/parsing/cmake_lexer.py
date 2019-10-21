import ply.lex as lex


class CMakeLexer:
    states = (
        ('commandinvocation', 'exclusive'),
    )

    tokens = ['NEWLINES',
              'UNHANDLED_YET',
              'LINE_COMMENT',
              'SPACES',
              'COMMAND_INVOCATION_START',
              'COMMAND_INVOCATION_END']

    t_LINE_COMMENT = r'\#[^\n]+'
    t_SPACES = r'[ \t]+'

    def __init__(self) -> None:
        self.lexer = lex.lex(module=self)

    @staticmethod
    def t_begin_commandinvocation(t: lex.Token) -> lex.Token:
        r"""[A-Za-z_][A-Za-z0-9_]*[ \t]*\("""
        t.type = 'COMMAND_INVOCATION_START'
        t.lexer.push_state('commandinvocation')
        return t

    @staticmethod
    def t_commandinvocation_end(t: lex.Token) -> lex.Token:
        r"""\)"""
        t.lexer.pop_state()
        t.type = 'COMMAND_INVOCATION_END'
        return t

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
