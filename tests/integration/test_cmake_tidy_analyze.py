###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from unittest import mock

from approvaltests.approvals import verify
from io import StringIO

from tests.integration.test_integration_base import TestIntegrationBase
from tests.integration.utils import execute_cmake_tidy, normalize, mangle_version


class TestCMakeTidyAnalyze(TestIntegrationBase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_analyze_command_help_shown(self, stdout):
        self.assertSuccess(execute_cmake_tidy(command='analyze', arguments=['--help']))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_analyze_should_correctly_print_version(self, stdout):
        self.assertSuccess(execute_cmake_tidy(None, arguments=['-v', 'analyze']))
        verify(mangle_version(stdout.getvalue()), self.reporter)
