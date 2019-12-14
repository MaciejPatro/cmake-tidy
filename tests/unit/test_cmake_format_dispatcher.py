import unittest

from cmake_tidy.formatting.cmake_format_dispatcher import CMakeFormatDispatcher


class TestCMakeFormatDispatcher(unittest.TestCase):
    def setUp(self) -> None:
        self.state = {}
        self.dispatcher = CMakeFormatDispatcher(self.state)

    def test_should_allow_to_setitem_for_dispatching(self):
        self.dispatcher['new'] = 1