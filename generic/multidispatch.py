""" Multidispatch for functions."""

import functools
import inspect
import types
import threading

from generic.registry import Registry
from generic.registry import TypeAxis

__all__ = ["Dispatcher", "multifunction"]


def multifunction(*argtypes):
    """ Declare function as multifunction."""
    def _replace_with_dispatcher(func):
        dispatcher = _make_dispatcher(Dispatcher, func, len(argtypes))
        dispatcher.register_rule(func, *argtypes)
        return dispatcher
    return _replace_with_dispatcher


def multimethod(*argtypes):
    """ Declare method as multimethod."""
    def _replace_with_dispatcher(func):
        dispatcher = _make_dispatcher(MethodDispatcher, func, len(argtypes) + 1)
        dispatcher.register_unbound_rule(func, *argtypes)
        return dispatcher
    return _replace_with_dispatcher


def has_multimethods(cls):
    """ Declare class as one that have multimethods."""
    for name, obj in cls.__dict__.items():
        if isinstance(obj, MethodDispatcher):
            obj.proceed_unbound_rules(cls)
    return cls


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

    def register_rule(self, rule, *argtypes):
        """ Register new ``rule`` for ``argtypes``."""
        # Check if we have the right number of parametrized types 
        if len(argtypes) != self.params_arity:
            raise TypeError("Wrong number of type parameters.")

        # Check if we have the same argspec (by number of args)
        rule_argspec = inspect.getargspec(rule)
        if not is_equalent_argspecs(rule_argspec, self.argspec):
            raise TypeError("Rule does not conform "
                            "to previous implementations.")

        self.registry.register(rule, *argtypes)

    def lookup_rule(self, *args):
        """ Lookup rule by ``args``. Returns None if no rule was found."""
        args = args[:self.params_arity]
        rule = self.registry.lookup(*args)
        if rule is None:
            raise TypeError("No available rule found for %r" % (args,))
        return rule

    def when(self, *argtypes):
        """ Parametrized decorator to register new rules with dispatcher."""
        def register_rule(func):
            self.register_rule(func, *argtypes)
            return self
        return register_rule

    def __call__(self, *args, **kwargs):
        """ Dispatch call to appropriate rule."""
        rule = self.lookup_rule(*args)
        return rule(*args, **kwargs)


class MethodDispatcher(Dispatcher):

    def __init__(self, argspec, params_arity):
        Dispatcher.__init__(self, argspec, params_arity)

        # some data, that should be local to thread of execution
        self.local = threading.local()
        self.local.unbound_rules = []

    def register_unbound_rule(self, func, *argtypes):
        self.local.unbound_rules.append((argtypes, func))

    def proceed_unbound_rules(self, cls):
        for argtypes, func in self.local.unbound_rules:
            argtypes = (cls,) + argtypes
            self.register_rule(func, *argtypes)
        self.local.unbound_rules = []

    def __get__(self, obj, cls):
        if obj is None:
            return self
        return types.MethodType(self, obj)

    def when(self, *argtypes):
        def make_declaration(meth):
            self.register_unbound_rule(meth, *argtypes)
            return self
        return make_declaration


def arity(argspec):
    """ Determinal positional arity of argspec."""
    args = argspec.args if argspec.args else []
    defaults = argspec.defaults if argspec.defaults else []
    return len(args) - len(defaults)


def is_equalent_argspecs(left, right):
    """ Check argspec equalence."""
    return map(lambda x: len(x) if x else 0, left) == \
           map(lambda x: len(x) if x else 0, right)


def _make_dispatcher(dispacther_cls, func, params_arity):
    argspec = inspect.getargspec(func)
    wrapper = functools.wraps(func)
    dispatcher = wrapper(dispacther_cls(argspec, params_arity))
    return dispatcher
