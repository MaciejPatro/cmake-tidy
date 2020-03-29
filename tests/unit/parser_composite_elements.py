###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from cmake_tidy.lexical_data.elements import Element, ComplexElement, PrimitiveElement


def spaces(data: str) -> PrimitiveElement:
    return PrimitiveElement('spaces', data)


def line_ending(comment, newlines_number):
    return ComplexElement('line_ending') \
        .add(PrimitiveElement('line_comment', comment)) \
        .add(PrimitiveElement('newlines', newlines_number))


def parentheses() -> Element:
    return ComplexElement('parentheses')


def newlines(number: int) -> Element:
    return ComplexElement('line_ending').add(PrimitiveElement('newlines', number))


def bracket_argument(bracket_size: int, data: str) -> Element:
    bracket_part = '=' * bracket_size
    return ComplexElement('bracket_argument') \
        .add(PrimitiveElement('bracket_start', f'[{bracket_part}[')) \
        .add(PrimitiveElement('bracket_argument_content', data)) \
        .add(PrimitiveElement('bracket_end', f']{bracket_part}]'))


def quoted_argument(data='') -> PrimitiveElement:
    return PrimitiveElement('quoted_argument', data)


def unquoted_argument(data='') -> PrimitiveElement:
    return PrimitiveElement('unquoted_argument', data)


def command_invocation(func_name: str, args=None):
    return ComplexElement('command_invocation') \
        .add(start_cmd(func_name)) \
        .add(args) \
        .add(end_cmd())


def file() -> Element:
    return ComplexElement('file')


def arguments() -> Element:
    return ComplexElement('arguments')


def start_cmd(name: str) -> PrimitiveElement:
    return PrimitiveElement('start_cmd_invoke', name)


def end_cmd() -> PrimitiveElement:
    return PrimitiveElement('end_cmd_invoke', ')')


def unhandled(data: str) -> PrimitiveElement:
    return PrimitiveElement('unhandled', data)
