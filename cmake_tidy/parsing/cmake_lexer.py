import ply.lex as lex


class CMakeLexer:
    states = (
        ('commandinvocation', 'exclusive'),
        ('bracketargument', 'exclusive'),
        ('quotedargument', 'exclusive')
    )

    tokens = ['NEWLINES',
              'UNHANDLED_YET',
              'LINE_COMMENT',
              'SPACES',
              'COMMAND_INVOCATION_START',
              'COMMAND_INVOCATION_END',
              'BRACKET_ARGUMENT_START',
              'BRACKET_ARGUMENT_CONTENT',
              'BRACKET_ARGUMENT_END',
              'QUOTED_ARGUMENT_START',
              'QUOTED_ARGUMENT_CONTENT',
              "QUOTED_ARGUMENT_END"]

    t_LINE_COMMENT = r'\#[^\n]+'
    t_SPACES = r'[ \t]+'

    def __init__(self) -> None:
        self.bracket_argument_size = 0
        self.lexer = lex.lex(module=self)

    @staticmethod
    def t_begin_commandinvocation(t: lex.Token) -> lex.Token:
        r"""[A-Za-z_][A-Za-z0-9_]*[ \t]*\("""
        t.type = 'COMMAND_INVOCATION_START'
        t.lexer.push_state('commandinvocation')
        return t

    def t_commandinvocation_begin_bracketargument(self, t: lex.Token) -> lex.Token:
        r"""\[==\["""
        t.type = 'BRACKET_ARGUMENT_START'
        self.bracket_argument_size = len(t.value)
        t.lexer.push_state('bracketargument')
        return t

    def t_commandinvocation_begin_quotedargument(self, t: lex.Token) -> lex.Token:
        r"""\""""
        t.type = 'QUOTED_ARGUMENT_START'
        t.lexer.push_state('quotedargument')
        return t

    @staticmethod
    def t_commandinvocation_end(t: lex.Token) -> lex.Token:
        r"""\)"""
        t.lexer.pop_state()
        t.type = 'COMMAND_INVOCATION_END'
        return t

    @staticmethod
    def t_quotedargument_end(t: lex.Token) -> lex.Token:
        r"""\""""
        t.lexer.pop_state()
        t.type = 'QUOTED_ARGUMENT_END'
        return t

    def t_bracketargument_end(self, t: lex.Token) -> lex.Token:
        r"""\]==\]"""
        if self.bracket_argument_size == len(t.value):
            t.lexer.pop_state()
            t.type = 'BRACKET_ARGUMENT_END'
        else:
            t.type = 'BRACKET_ARGUMENT_CONTENT'
        return t

    @staticmethod
    def t_NEWLINES(t: lex.LexToken) -> lex.LexToken:
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        return t

    @staticmethod
    def t_INITIAL_commandinvocation_error(t: lex.LexToken) -> lex.LexToken:
        t.lexer.skip(1)
        t.type = 'UNHANDLED_YET'
        t.value = t.value[0]
        return t

    @staticmethod
    def t_bracketargument_error(t: lex.LexToken) -> lex.LexToken:
        t.lexer.skip(1)
        t.type = 'BRACKET_ARGUMENT_CONTENT'
        t.value = t.value[0]
        return t

    @staticmethod
    def t_quotedargument_error(t: lex.LexToken) -> lex.LexToken:
        t.lexer.skip(1)
        t.type = 'QUOTED_ARGUMENT_CONTENT'
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
