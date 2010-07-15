""" Multidispatch for functions."""

import functools
import inspect

from generic.registry import Registry
from generic.registry import TypeAxis

__all__ = ["Dispatcher", "multimethod"]


def multimethod(*arg_types):
    """ Declare function as multimethod."""
    def register_rule(func):
        argspec = inspect.getargspec(func)
        wrapper = functools.wraps(func)
        dispatcher = wrapper(Dispatcher(argspec, len(arg_types)))
        dispatcher.register_rule(func, *arg_types)
        return dispatcher
    return register_rule


def arity(argspec):
    """ Determinal positional arity of argspec."""
    args = argspec.args if argspec.args else []
    defaults = argspec.defaults if argspec.defaults else []
    return len(args) - len(defaults)


def is_equalent_argspecs(left, right):
    """ Check argspec equalence."""
    return map(lambda x: len(x) if x else 0, left) == \
           map(lambda x: len(x) if x else 0, right)


class Dispatcher(object):
    """ Function call dispatcher based on argument types."""

    def __init__(self, argspec, params_arity):
        """ Initialize dispatcher with ``argspec`` of type
        :class:`inspect.ArgSpec` and ``params_arity`` that represent number
        params."""
        # Check if we have enough positional arguments for number of type params
        if arity(argspec) < params_arity:
            raise TypeError("Not enough positional arguments "
                            "for number of type parameters provided.")

        self.argspec = argspec
        self.params_arity = params_arity

        axis = [("arg_%d" % n, TypeAxis()) for n in range(params_arity)]
        self.registry = Registry(*axis)

    def register_rule(self, rule, *arg_types):
        """ Register new ``rule`` for ``arg_types``."""
        # Check if we have the right number of parametrized types 
        if len(arg_types) != self.params_arity:
            raise TypeError("Wrong number of type parameters.")

        # Check if we have the same argspec (by number of args)
        rule_argspec = inspect.getargspec(rule)
        if not is_equalent_argspecs(rule_argspec, self.argspec):
            raise TypeError("Rule does not conform "
                            "to previous implementations.")

        self.registry.register(rule, *arg_types)

    def lookup_rule(self, *args):
        """ Lookup rule by ``args``. Returns None if no rule was found."""
        args = args[:self.params_arity]
        return self.registry.lookup(*args)

    def when(self, *arg_types):
        """ Parametrized decorator to register new rules with dispatcher."""
        def register_rule(func):
            self.register_rule(func, *arg_types)
            return self
        return register_rule

    def __call__(self, *args, **kwargs):
        """ Dispatch call to appropriate rule."""
        rule = self.lookup_rule(*args)
        if rule is None:
            raise TypeError("No available rule found for %r" % (args,))
        return rule(*args, **kwargs)
