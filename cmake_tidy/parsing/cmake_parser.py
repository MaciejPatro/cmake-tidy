###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import ply.yacc as yacc

from cmake_tidy.parsing.cmake_lexer import CMakeLexer
from cmake_tidy.lexical_data.elements import PrimitiveElement, ComplexElement


class ParsingError(Exception):
    pass


class CMakeParser:
    def __init__(self) -> None:
        self.lexer = CMakeLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.__lineno = 1

    @staticmethod
    def p_file(p):
        """file : file file_element
                | file_element
                | empty"""
        if p[1].name == 'file':
            p[0] = p[1].add(p[2])
        else:
            p[0] = ComplexElement('file').add(p[1])

    @staticmethod
    def p_file_element(p):
        """file_element : line_ending
                        | spaces
                        | command_invocation"""
        p[0] = p[1]

    @staticmethod
    def p_command_invocation(p):
        """command_invocation : start_cmd_invoke arguments end_cmd_invoke"""
        p[0] = ComplexElement('command_invocation')
        for element in p[1:]:
            p[0].add(element)

    @staticmethod
    def p_parentheses(p):
        """parentheses : start_parenthesis arguments end_parenthesis"""
        p[0] = ComplexElement('parentheses')
        for element in p[1:]:
                p[0].add(element)

    @staticmethod
    def p_arguments(p):
        """arguments : arguments argument
                     | argument"""
        if p[1].name == 'arguments':
            p[0] = p[1].add(p[2])
        else:
            p[0] = ComplexElement('arguments').add(p[1])

    @staticmethod
    def p_argument(p):
        """argument : bracket_argument
                    | quoted_argument
                    | unquoted_argument
                    | arguments_separation
                    | parentheses
                    | empty"""
        p[0] = p[1]

    @staticmethod
    def p_arguments_separation(p):
        """arguments_separation : spaces
                                | line_ending"""
        p[0] = p[1]

    @staticmethod
    def p_quoted_argument(p):
        """quoted_argument : QUOTED_ARGUMENT_START quoted_argument_content QUOTED_ARGUMENT_END"""
        p[0] = PrimitiveElement('quoted_argument', p[2].values)

    @staticmethod
    def p_bracket_argument(p):
        """bracket_argument : BRACKET_ARGUMENT_START bracket_argument_content BRACKET_ARGUMENT_END"""
        p[0] = ComplexElement('bracket_argument') \
            .add(PrimitiveElement('bracket_start', p[1])) \
            .add(PrimitiveElement('bracket_argument_content', p[2].values)) \
            .add(PrimitiveElement('bracket_end', p[3]))

    @staticmethod
    def p_line_ending(p):
        """line_ending : line_comment newlines
                       | newlines"""
        p[0] = ComplexElement('line_ending')
        for element in p[1:]:
            p[0].add(element)

    @staticmethod
    def p_unquoted_argument(p):
        """unquoted_argument : UNQUOTED_ARGUMENT"""
        p[0] = PrimitiveElement('unquoted_argument', p[1])

    @staticmethod
    def p_line_comment(p):
        """line_comment : LINE_COMMENT"""
        p[0] = PrimitiveElement('line_comment', p[1])

    def p_newlines(self, p):
        """newlines : NEWLINES"""
        newlines = len(p[1])
        self.__lineno += newlines
        p[0] = PrimitiveElement('newlines', newlines)

    @staticmethod
    def p_empty(p):
        """empty :"""
        p[0] = PrimitiveElement()

    @staticmethod
    def p_bracket_argument_content(p):
        """bracket_argument_content : bracket_argument_content bracket_argument_content_element
                                    | bracket_argument_content_element"""
        _create_content(p, 'bracket_argument_content')

    @staticmethod
    def p_quoted_argument_content(p):
        """quoted_argument_content : quoted_argument_content quoted_argument_content_element
                                   | quoted_argument_content_element
                                   | empty"""
        _create_content(p, 'quoted_argument_content')

    @staticmethod
    def p_bracket_argument_content_element(p):
        """bracket_argument_content_element : BRACKET_ARGUMENT_CONTENT"""
        p[0] = _get_content_element(p[1])

    @staticmethod
    def p_quoted_argument_content_element(p):
        """quoted_argument_content_element : QUOTED_ARGUMENT_CONTENT"""
        p[0] = _get_content_element(p[1])

    @staticmethod
    def p_spaces(p):
        """spaces : SPACES"""
        p[0] = PrimitiveElement('spaces', p[1])

    @staticmethod
    def p_start_parenthesis(p):
        """start_parenthesis : BEGIN_PARENTHESIS"""
        p[0] = PrimitiveElement('parenthesis_start', p[1])

    @staticmethod
    def p_end_parenthesis(p):
        """end_parenthesis : END_PARENTHESIS"""
        p[0] = PrimitiveElement('parenthesis_end', p[1])

    @staticmethod
    def p_start_cmd_invoke(p):
        """start_cmd_invoke : COMMAND_INVOCATION_START"""
        p[0] = PrimitiveElement('start_cmd_invoke', p[1])

    @staticmethod
    def p_end_cmd_invoke(p):
        """end_cmd_invoke : COMMAND_INVOCATION_END"""
        p[0] = PrimitiveElement('end_cmd_invoke', p[1])

    def p_error(self, p):
        if p is not None:
            raise ParsingError(f'Illegal symbol in line {self.__lineno}: \"{p.value}\"')
        raise ParsingError('Missing symbol - some invocation is not properly finished')

    def parse(self, data: str):
        return self.parser.parse(data)


def _get_content_element(data) -> PrimitiveElement:
    return PrimitiveElement('content_element', str(data))


def _create_content(p, name: str):
    if p[1].name is name:
        p[0] = p[1]
        p[0].values += p[2].values
    else:
        p[0] = PrimitiveElement(name, p[1].values)
