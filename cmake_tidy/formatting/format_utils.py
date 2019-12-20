import re

_reindent_token = '<cmake-tidy-reindent>'


class FormatNewline:
    def __init__(self, state: dict, settings: dict):
        self.__state = state
        self.__settings = settings

    def __call__(self, data) -> str:
        return self.__format_newlines(data) + self.__prepare_initial_newline_indent()

    def __prepare_initial_newline_indent(self) -> str:
        return self.__state['indent'] * self.__settings['tab_size'] * ' '

    def __format_newlines(self, number_of_newlines: int) -> str:
        return '\n' * min(self.__settings['succeeding_newlines'], number_of_newlines)


class FormatStartCommandInvocation:
    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        self.__state['indent'] += 1
        return data


class FormatCommandInvocation:
    __start_tokens = ['macro', 'while', 'foreach', 'if', 'function']
    __reindent_commands = ['endfunction', 'endif', 'elseif', 'endwhile', 'endforeach', 'endmacro',
                           'else']

    def __init__(self, state: dict):
        self.__state = state

    def __call__(self, data) -> str:
        original = ''.join(data)
        self.__update_indentation(original)
        return self.__add_reindent_tokens_where_needed(original)

    def __update_indentation(self, formatted):
        if not self.__is_start_of_special_command(formatted):
            self.__state['indent'] -= 1
        if self.__is_end_of_special_command(formatted):
            self.__state['indent'] -= 1

    @staticmethod
    def __is_start_of_special_command(original: str) -> bool:
        return any([original.startswith(f'{token}(') for token in FormatCommandInvocation.__start_tokens])

    @staticmethod
    def __is_end_of_special_command(original: str) -> bool:
        return any([original.startswith(f'end{token}(') for token in FormatCommandInvocation.__start_tokens])

    @staticmethod
    def __add_reindent_tokens_where_needed(original: str) -> str:
        for reindent_cmd in FormatCommandInvocation.__reindent_commands:
            if original.startswith(f'{reindent_cmd}('):
                return _reindent_token + original
        return original


class FormatFile:
    def __init__(self, settings: dict):
        self.__settings = settings

    def __call__(self, data) -> str:
        return self.__cleanup_end_invocations(''.join(data))

    def __cleanup_end_invocations(self, formatted_file: str) -> str:
        indent = self.__settings['tab_size'] * ' '
        formatted_file = formatted_file.replace(indent + _reindent_token, '')
        return formatted_file


class FormatSpaces:
    def __init__(self, settings: dict, state: dict):
        self.__settings = settings
        self.__state = state

    def __call__(self, data) -> str:
        if self.__state['last'] is 'line_ending':
            return ''
        return data.replace('\t', ' ' * self.__settings['tab_size'])


class FormatArguments:
    __spacing = r'^[ \t]+$'

    def __call__(self, data) -> str:
        if data[0]:
            data = self.__replace_spacings_between_arguments_with_single_space(data)
            data = self.__remove_spacing_from_first_element(data)
            data = self.__remove_spacing_from_last_element(data)
            return ''.join(data)
        return ''

    @staticmethod
    def __replace_spacings_between_arguments_with_single_space(data: list) -> list:
        return [re.sub(FormatArguments.__spacing, ' ', element) for element in data]

    @staticmethod
    def __remove_spacing_from_first_element(data: list) -> list:
        return data[1:] if re.match(FormatArguments.__spacing, data[0]) else data

    @staticmethod
    def __remove_spacing_from_last_element(data: list) -> list:
        return data[:-1] if re.match(FormatArguments.__spacing, data[-1]) else data
