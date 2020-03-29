###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


from unittest import mock

from approvaltests.approvals import verify
from io import StringIO

from tests.integration.test_integration_base import TestIntegrationBase
from tests.integration.utils import execute_cmake_tidy, normalize


class TestCMakeTidy(TestIntegrationBase):
    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_incorrect_command_should_print_error_with_usage_help(self, stdout):
        self.assertFail(execute_cmake_tidy(command='', arguments=[]))
        normalized_output = normalize(stdout.getvalue())
        verify(normalized_output, self.reporter)
