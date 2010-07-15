""" Multidispatch for functions."""

import functools
import inspect

from generic.registry import Registry
from generic.registry import TypeAxis

__all__ = ["Dispatcher", "multimethod", "reset"]

# function name -> dispatcher
dispatchers = {}


def multimethod(*arg_types):
    """ Declare function as multimethod."""
    global dispatchers
    def register_rule(func):
        if func.__name__ in dispatchers:
            dispatcher = dispatchers[func.__name__]
        else:
            dispatcher = functools.wraps(func)(Dispatcher(len(arg_types)))
            dispatchers[func.__name__] = dispatcher
        dispatcher.register_rule(func, *arg_types)
        return dispatcher
    return register_rule


def reset():
    """ Reset dispatchers. Useful for testing."""
    global dispatchers
    dispatchers = {}


class Dispatcher(object):
    """ Function call dispatcher based on argument types."""

    def __init__(self, arity):
        self.arity = arity
        axis = [("arg_%d" % n, TypeAxis()) for n in range(arity)]
        self.registry = Registry(*axis)

    def register_rule(self, rule, *args):
        self.check_rule(rule)
        self.registry.register(rule, *args)

    def lookup_rule(self, *args):
        return self.registry.lookup(*args)

    def check_rule(self, rule):
        argspec = inspect.getargspec(rule)
        if argspec.defaults:
            raise NotImplementedError("Keyword argument support "
                                      "not implemented yet.")
        if not len(argspec.args) == self.arity:
            raise TypeError("Rule does not conform "
                            "to previous implementations.")

    def __call__(self, *args):
        rule = self.lookup_rule(*args)
        if rule is None:
            raise TypeError("No avaible rule found for %r" % (args,))
        return rule(*args)
