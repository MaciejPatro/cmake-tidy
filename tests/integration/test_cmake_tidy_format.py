from unittest import mock
import unittest

from approvaltests.approvals import verify
from io import StringIO

from tests.integration.test_integration_base import TestIntegrationBase
from tests.integration.utils import execute_cmake_tidy, normalize


class TestCMakeTidyFormat(TestIntegrationBase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_command_help_shown(self, stdout):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--help']))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_incorrect_command_should_print_error_with_usage_help(self, stdout):
        self.assertFail(execute_cmake_tidy(command='format', arguments=[]))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @unittest.SkipTest
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_should_dump_config_only_configuration_to_stdout_by_default(self, stdout):
        self.assertSuccess(execute_cmake_tidy(command='format', arguments=['--dump-config', 'dummy.txt']))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)
