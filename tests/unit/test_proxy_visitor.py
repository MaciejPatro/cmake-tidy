import unittest

from cmake_tidy.utils.proxy_visitor import ProxyVisitor


class TestProxyVisitor(unittest.TestCase):
    @staticmethod
    def __private_function_with_int_argument(number: int) -> str:
        return str(number)

    class SimpleFunctor:
        def __init__(self):
            self.state = False

        def __call__(self, x: str) -> None:
            self.state = True

    def setUp(self):
        self.function_dict = {'private': self.__private_function_with_int_argument}

    def test_private_function_invoked_in_proxy(self):
        proxy = ProxyVisitor(self.function_dict)
        self.assertEqual('5', proxy.visit('private', 5))

    def test_lambda_invocation_in_proxy(self):
        self.function_dict['lambda'] = lambda a: a[0] + a[1]
        proxy = ProxyVisitor(self.function_dict)
        self.assertEqual(6, proxy.visit('lambda', [2, 4]))

    def test_functor_preserving_state(self):
        functor = self.SimpleFunctor()
        self.function_dict['functor'] = functor
        proxy = ProxyVisitor(self.function_dict)
        proxy.visit('functor')
        self.assertTrue(functor.state)
