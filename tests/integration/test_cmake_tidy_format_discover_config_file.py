###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import json
import tempfile
from pathlib import Path
from unittest import mock

from io import StringIO

from cmake_tidy.formatting import SettingsReader
from tests.integration.test_integration_base import TestIntegrationBase
from tests.integration.utils import execute_cmake_tidy


class TestCMakeTidyFormatDiscoverConfigFile(TestIntegrationBase):
    def setUp(self):
        super(TestCMakeTidyFormatDiscoverConfigFile, self).setUp()
        self.default_settings = SettingsReader.get_default_format_settings()
        self.temp_directory = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def create_config_file(self, directory: Path, data: str):
        config_file = directory
        config_file.mkdir(parents=True, exist_ok=False)
        config_file = config_file / '.cmake-tidy.json'
        with config_file.open('w') as f:
            f.write(data)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_default_config_when_no_config_available_in_cwd(self, stdout):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config']))
        self.assertDictEqual(self.default_settings, json.loads(stdout.getvalue()))

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_config_from_current_cwd(self, stdout):
        fake_path = Path(self.temp_directory.name) / 'abc'
        self.create_config_file(fake_path, '{"line_length": 20}')

        with mock.patch('pathlib.Path.cwd', return_value=fake_path):
            self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config']))
            received_settings = json.loads(stdout.getvalue())
            self.assertFalse(self.default_settings == received_settings)
            self.assertEqual(20, received_settings.get('line_length'))

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_config_from_input_file_location_as_config_is_there(self, stdout):
        fake_path = Path(self.temp_directory.name) / 'some_dir'
        self.create_config_file(fake_path, '{"line_length": 40}')
        input_filename = str((fake_path / 'test.cmake').absolute())

        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config', input_filename]))
        received_settings = json.loads(stdout.getvalue())
        self.assertFalse(self.default_settings == received_settings)
        self.assertEqual(40, received_settings.get('line_length'))

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_config_from_one_of_input_file_parents_location(self, stdout):
        fake_path = Path(self.temp_directory.name) / 'some_dir'
        self.create_config_file(fake_path, '{"line_length": 33}')
        input_filename = str((fake_path / 'another' / 'test.cmake').absolute())

        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config', input_filename]))
        received_settings = json.loads(stdout.getvalue())
        self.assertFalse(self.default_settings == received_settings)
        self.assertEqual(33, received_settings.get('line_length'))

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_config_from_one_of_input_file_parents_location_priority_close_to_file(self, stdout):
        fake_path = Path(self.temp_directory.name) / 'some_dir'
        self.create_config_file(fake_path, '{"line_length": 33}')
        self.create_config_file(fake_path / 'another', '{"line_length": 32}')
        input_filename = str((fake_path / 'another' / 'yet_something' / 'test.cmake').absolute())

        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config', input_filename]))
        received_settings = json.loads(stdout.getvalue())
        self.assertFalse(self.default_settings == received_settings)
        self.assertEqual(32, received_settings.get('line_length'))
