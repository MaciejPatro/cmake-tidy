###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import json
from json import JSONDecodeError
from pathlib import Path
from jsonschema import Draft6Validator, SchemaError, ValidationError


class InvalidSchemaError(Exception):
    pass


class SchemaValidationError(ValidationError):
    pass


class SettingsReader:
    def __init__(self):
        self.__schema = self.__try_reading_schema()
        self.__settings = self.get_default_format_settings()

    def try_loading_format_settings(self) -> dict:
        self.__settings.update(self.__try_reading_settings())
        return self.__settings

    def __try_reading_settings(self) -> dict:
        try:
            user_define_settings = self._read_settings()
            self.__schema.validate(user_define_settings)
            return user_define_settings
        except (ValidationError, JSONDecodeError) as error:
            raise SchemaValidationError(str(error))

    def __try_reading_schema(self) -> Draft6Validator:
        try:
            schema = self._read_schema_file()
            Draft6Validator.check_schema(schema)
            return Draft6Validator(schema)
        except (FileNotFoundError, OSError, SchemaError, JSONDecodeError):
            raise InvalidSchemaError('JSON schema validation error - please raise issue on github!')

    @staticmethod
    def _read_schema_file() -> dict:
        schema_file = Path(__file__).parent / 'settings.json'
        with schema_file.open() as file:
            return json.load(file)

    @staticmethod
    def _read_settings() -> dict:
        settings_file = Path.cwd() / '.cmake-tidy.json'
        if settings_file.exists() and settings_file.stat().st_size > 0:
            with settings_file.open() as file:
                return json.load(file)
        return dict()

    @staticmethod
    def get_default_format_settings() -> dict:
        settings = dict()
        settings['succeeding_newlines'] = 2
        settings['tabs_as_spaces'] = False
        settings['tab_size'] = 4
        settings['force_command_lowercase'] = True
        settings['space_between_command_and_begin_parentheses'] = False
        settings['line_length'] = 100
        settings['wrap_short_invocations_to_single_line'] = True
        settings['closing_parentheses_in_newline_when_split'] = True
        settings['unquoted_uppercase_as_keyword'] = False
        settings['space_after_loop_condition'] = False
        settings['keep_property_and_value_in_one_line'] = True
        settings['keyword_and_single_value_in_one_line'] = True
        settings['keep_command_in_single_line'] = True
        settings['condition_splitting_move_and_or_to_newline'] = True
        settings['keywords'] = []
        return settings
