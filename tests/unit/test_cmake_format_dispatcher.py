###############################################################################
# Copyright Maciej Patro (maciej.patro@gmail.com)
# MIT License
###############################################################################


import unittest

from cmake_tidy.formatting.cmake_format_dispatcher import CMakeFormatDispatcher


class TestCMakeFormatDispatcher(unittest.TestCase):
    def setUp(self) -> None:
        self.state = {'last': None}
        self.dispatcher = CMakeFormatDispatcher(self.state)

    def assertLastStateEqual(self, value):
        self.assertEqual(self.state['last'], value)

    def test_state_should_not_be_changed_when_object_created(self):
        self.assertLastStateEqual(None)

    def test_dispatched_method_should_remember_last_usage(self):
        self.dispatcher['new'] = lambda: 1
        self.assertEqual(1, self.dispatcher['new']())
        self.assertLastStateEqual('new')

    def test_ensure_that_state_changes_at_the_end_of_invocation(self):
        self.dispatcher['some'] = lambda: self.state['last']
        self.assertEqual(None, self.dispatcher['some']())
        self.assertLastStateEqual('some')

    def test_dispatcher_should_accept_only_callable_values(self):
        with self.assertRaises(TypeError):
            self.dispatcher['value'] = 1

    def test_dispatcher_should_raise_key_error_when_no_such_key(self):
        with self.assertRaises(KeyError):
            self.dispatcher['x']
