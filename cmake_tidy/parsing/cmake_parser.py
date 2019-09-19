import ply.yacc as yacc

from cmake_tidy.parsing.cmake_lexer import CMakeLexer
from cmake_tidy.parsing.elements import PrimitiveElement, ComplexElement


class CMakeParser:
    def __init__(self) -> None:
        self.lexer = CMakeLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    @staticmethod
    def p_file(p):
        """file : file file_element
                | file_element
                | empty"""
        if p[1].name is 'file':
            p[0] = p[1].add(p[2])
        else:
            p[0] = ComplexElement('file').add(p[1])

    @staticmethod
    def p_file_element(p):
        """file_element : newlines
                        | unhandled"""
        p[0] = p[1]

    @staticmethod
    def p_newlines(p):
        """newlines : NEWLINES"""
        p[0] = PrimitiveElement('newlines', len(p[1]))

    @staticmethod
    def p_empty(p):
        """empty :"""
        p[0] = PrimitiveElement()

    @staticmethod
    def p_unhandled(p):
        """unhandled : UNHANDLED_YET"""
        p[0] = PrimitiveElement('unhandled', p[1])

    @staticmethod
    def p_error(p):
        print("Illegal symbol '%s'" % p.type)

    def parse(self, data: str):
        return self.parser.parse(data)
