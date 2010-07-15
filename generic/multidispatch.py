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
        argspec = inspect.getargspec(func)
        if func.__name__ in dispatchers:
            dispatcher = dispatchers[func.__name__]
        else:
            dispatcher = functools.wraps(func)(
                Dispatcher(argspec, len(arg_types)))
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

    def __init__(self, argspec, multi_arity):
        pos_arity = \
            len(argspec.args if argspec.args else []) - \
            len(argspec.defaults if argspec.defaults else [])
        if pos_arity < multi_arity:
            raise TypeError("Not enough positional arguments "
                            "for number of type parameters provided.")
        self.argspec = argspec
        self.multi_arity = multi_arity
        axis = [("arg_%d" % n, TypeAxis()) for n in range(multi_arity)]
        self.registry = Registry(*axis)

    def register_rule(self, rule, *args):
        if len(args) != self.multi_arity:
            raise TypeError("Wrong number of type parameters.")
        self.check_rule(rule)
        self.registry.register(rule, *args)

    def lookup_rule(self, *args):
        return self.registry.lookup(*args[:self.multi_arity])

    def check_rule(self, rule):
        argspec = inspect.getargspec(rule)
        if not map(lambda x: len(x) if x else 0, argspec) == \
          map(lambda x: len(x) if x else 0, self.argspec):
            raise TypeError("Rule does not conform "
                            "to previous implementations.")

    def __call__(self, *args):
        rule = self.lookup_rule(*args)
        if rule is None:
            raise TypeError("No avaible rule found for %r" % (args,))
        return rule(*args)
