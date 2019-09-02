import ply.yacc as yacc

from cmake_tidy.parsing.cmake_lexer import CMakeLexer
from cmake_tidy.parsing.elements import PrimitiveElement


class CMakeParser:
    def __init__(self) -> None:
        self.lexer = CMakeLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    @staticmethod
    def p_empty(p):
        """empty :"""
        p[0] = PrimitiveElement()

    @staticmethod
    def p_error(p):
        print("Illegal symbol '%s'" % p.type)

    def parse(self, data: str):
        return self.parser.parse(data)
