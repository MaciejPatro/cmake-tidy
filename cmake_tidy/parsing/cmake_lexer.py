###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import ply.lex as lex


class CMakeLexer:
    states = (
        ('commandinvocation', 'exclusive'),
        ('bracketargument', 'exclusive'),
        ('quotedargument', 'exclusive'),
        ('insideparentheses', 'exclusive')
    )
    tokens = ['NEWLINES',
              'LINE_COMMENT',
              'SPACES',
              'COMMAND_INVOCATION_START',
              'COMMAND_INVOCATION_END',
              'BRACKET_ARGUMENT_START',
              'BRACKET_ARGUMENT_CONTENT',
              'BRACKET_ARGUMENT_END',
              'QUOTED_ARGUMENT_START',
              'QUOTED_ARGUMENT_CONTENT',
              'QUOTED_ARGUMENT_END',
              'UNQUOTED_ARGUMENT',
              'BEGIN_PARENTHESIS',
              'END_PARENTHESIS']

    t_INITIAL_commandinvocation_insideparentheses_LINE_COMMENT = r'\#((?=\n)|[^\n]+)'
    t_INITIAL_commandinvocation_insideparentheses_SPACES = r'[ \t]+'
    t_quotedargument_QUOTED_ARGUMENT_CONTENT = r'(?<!\\)\\\"'
    t_commandinvocation_insideparentheses_UNQUOTED_ARGUMENT = r'[^ \t\(\)\#\"\\\n]+'

    def __init__(self) -> None:
        self.bracket_argument_size = -1
        self.lexer = lex.lex(module=self)

    @staticmethod
    def t_begin_commandinvocation(t: lex.Token) -> lex.Token:
        r"""[A-Za-z_][A-Za-z0-9_]*[ \t]*\("""
        t.type = 'COMMAND_INVOCATION_START'
        t.lexer.push_state('commandinvocation')
        return t

    def t_commandinvocation_insideparentheses_begin_insideparentheses(self, t: lex.Token) -> lex.Token:
        r"""\("""
        t.type = 'BEGIN_PARENTHESIS'
        t.lexer.push_state('insideparentheses')
        return t

    def t_commandinvocation_insideparentheses_begin_bracketargument(self, t: lex.Token) -> lex.Token:
        r"""\[=*\["""
        t.type = 'BRACKET_ARGUMENT_START'
        self.bracket_argument_size = len(t.value)
        t.lexer.push_state('bracketargument')
        return t

    def t_commandinvocation_insideparentheses_begin_quotedargument(self, t: lex.Token) -> lex.Token:
        r"""\""""
        t.type = 'QUOTED_ARGUMENT_START'
        t.lexer.push_state('quotedargument')
        return t

    @staticmethod
    def t_commandinvocation_end(t: lex.Token) -> lex.Token:
        r"""\)"""
        return _end_state(t, 'COMMAND_INVOCATION_END')

    @staticmethod
    def t_insideparentheses_end(t: lex.Token) -> lex.Token:
        r"""\)"""
        return _end_state(t, 'END_PARENTHESIS')

    @staticmethod
    def t_quotedargument_end(t: lex.Token) -> lex.Token:
        r"""\""""
        return _end_state(t, 'QUOTED_ARGUMENT_END')

    def t_bracketargument_end(self, t: lex.Token) -> lex.Token:
        r"""\]=*\]"""
        if self.bracket_argument_size == len(t.value):
            t.lexer.pop_state()
            t.type = 'BRACKET_ARGUMENT_END'
        else:
            t.type = 'BRACKET_ARGUMENT_CONTENT'
        return t

    @staticmethod
    def t_INITIAL_commandinvocation_insideparentheses_NEWLINES(t: lex.LexToken) -> lex.LexToken:
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        return t

    @staticmethod
    def t_INITIAL_commandinvocation_insideparentheses_error(t: lex.LexToken) -> lex.LexToken:
        return _skip_one_and_return_with(t, '?')

    @staticmethod
    def t_bracketargument_error(t: lex.LexToken) -> lex.LexToken:
        return _skip_one_and_return_with(t, 'BRACKET_ARGUMENT_CONTENT')

    @staticmethod
    def t_quotedargument_error(t: lex.LexToken) -> lex.LexToken:
        return _skip_one_and_return_with(t, 'QUOTED_ARGUMENT_CONTENT')

    def analyze(self, data: str) -> list:
        self.lexer.input(data)
        data = []

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            data.append(tok)

        return data


def _skip_one_and_return_with(element: lex.LexToken, token_type: str) -> lex.LexToken:
    element.lexer.skip(1)
    element.type = token_type
    element.value = element.value[0]
    return element


def _end_state(element: lex.LexToken, token_type: str) -> lex.LexToken:
    element.lexer.pop_state()
    element.type = token_type
    return element
