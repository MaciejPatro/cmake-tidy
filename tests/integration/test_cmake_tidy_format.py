import unittest
import mock

from approvaltests.approvals import verify
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
from io import StringIO

from tests.integration.utils import execute_cmake_tidy


class TestCMakeTidyFormat(unittest.TestCase):
    def setUp(self):
        self.reporter = GenericDiffReporterFactory().get_first_working()

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_format_command_help_shown(self, stdout):
        execute_cmake_tidy(command='format', arguments=['--help'])
        verify(stdout.getvalue(), self.reporter)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_incorrect_command_should_print_error_with_usage_help(self, stdout):
        execute_cmake_tidy(command='', arguments=[])
        verify(stdout.getvalue(), self.reporter)
