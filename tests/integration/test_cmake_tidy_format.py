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
    def test_format_command(self, stdout):
        execute_cmake_tidy(command='format', arguments=[])
        verify(stdout.getvalue(), self.reporter)
