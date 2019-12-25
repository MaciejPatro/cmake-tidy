import unittest

from approvaltests.reporters import GenericDiffReporterFactory


class TestIntegrationBase(unittest.TestCase):
    def setUp(self):
        self.reporter = GenericDiffReporterFactory().get_first_working()

    def assertSuccess(self, exit_code):
        self.assertEqual(0, exit_code)

    def assertFail(self, exit_code):
        self.assertNotEqual(0, exit_code)
