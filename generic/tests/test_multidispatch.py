""" Tests for :module:`generic.multidispatch`."""

import unittest

__all__ = []


class DispatcherTests(unittest.TestCase):

    def test_one_argument(self):
        from generic.multidispatch import Dispatcher
        dispatcher = Dispatcher(1)

        dispatcher.register_rule(lambda x: x + 1, int)
        self.assertEqual(dispatcher(1), 2)
        self.assertRaises(TypeError, dispatcher.__call__, "s")

        dispatcher.register_rule(lambda x: x + "1", str)
        self.assertEqual(dispatcher(1), 2)
        self.assertEqual(dispatcher("1"), "11")
        self.assertRaises(TypeError, dispatcher.__call__, tuple())

    def test_two_arguments(self):
        from generic.multidispatch import Dispatcher
        dispatcher = Dispatcher(2)

        dispatcher.register_rule(lambda x, y: x + y + 1, int, int)
        self.assertEqual(dispatcher(1, 2), 4)
        self.assertRaises(TypeError, dispatcher.__call__, "s", "ss")
        self.assertRaises(TypeError, dispatcher.__call__, 1, "ss")
        self.assertRaises(TypeError, dispatcher.__call__, "s", 2)

        dispatcher.register_rule(lambda x, y: x + y + "1", str, str)
        self.assertEqual(dispatcher(1, 2), 4)
        self.assertEqual(dispatcher("1", "2"), "121")
        self.assertRaises(TypeError, dispatcher.__call__, "1", 1)
        self.assertRaises(TypeError, dispatcher.__call__, 1, "1")

        dispatcher.register_rule(lambda x, y: str(x) + y + "1", int, str)
        self.assertEqual(dispatcher(1, 2), 4)
        self.assertEqual(dispatcher("1", "2"), "121")
        self.assertEqual(dispatcher(1, "2"), "121")
        self.assertRaises(TypeError, dispatcher.__call__, "1", 1)

    def test_bottom_rule(self):
        from generic.multidispatch import Dispatcher
        dispatcher = Dispatcher(1)

        dispatcher.register_rule(lambda x: x, object)
        self.assertEqual(dispatcher(1), 1)
        self.assertEqual(dispatcher("1"), "1")
        self.assertEqual(dispatcher([1]), [1])
        self.assertEqual(dispatcher((1,)), (1,))

    def test_subtype_evaluation(self):
        class Super(object):
            pass
        class Sub(Super):
            pass

        from generic.multidispatch import Dispatcher
        dispatcher = Dispatcher(1)

        dispatcher.register_rule(lambda x: x, Super)
        o_super = Super()
        self.assertEqual(dispatcher(o_super), o_super)
        o_sub = Sub()
        self.assertEqual(dispatcher(o_sub), o_sub)
        self.assertRaises(TypeError, dispatcher.__call__, object())

        dispatcher.register_rule(lambda x: (x, x), Sub)
        o_super = Super()
        self.assertEqual(dispatcher(o_super), o_super)
        o_sub = Sub()
        self.assertEqual(dispatcher(o_sub), (o_sub, o_sub))

    def test_register_rule_with_different_arity(self):
        from generic.multidispatch import Dispatcher
        dispatcher = Dispatcher(1)
        dispatcher.register_rule(lambda x: x, int)
        self.assertRaises(TypeError, dispatcher.register_rule, lambda x, y: x)

    def test_register_rule_wit_kw_args(self):
        # Keyword args do not supported right now.
        from generic.multidispatch import Dispatcher
        dispatcher = Dispatcher(1)
        self.assertRaises(
            NotImplementedError,
            dispatcher.register_rule, lambda x=1: x)


class TestMultimethod(unittest.TestCase):

    def tearDown(self):
        from generic.multidispatch import reset
        reset()

    def test_it(self):
        from generic.multidispatch import multimethod

        @multimethod(int, str)
        def func(x, y):
            return str(x) + y

        self.assertEqual(func(1, "2"), "12")
        self.assertRaises(TypeError, func, 1, 2)
        self.assertRaises(TypeError, func, "1", 2)
        self.assertRaises(TypeError, func, "1", "2")

        @multimethod(str, str)
        def func(x, y):
            return x + y

        self.assertEqual(func(1, "2"), "12")
        self.assertEqual(func("1", "2"), "12")
        self.assertRaises(TypeError, func, 1, 2)
        self.assertRaises(TypeError, func, "1", 2)
