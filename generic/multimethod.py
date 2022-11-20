"""Multi-method builds on the functionality provided by `multidispatch` to
provide generic methods."""

from __future__ import annotations

import functools
import inspect
import threading
import types
from typing import Any, Callable, TypeVar, Union, cast

from generic.multidispatch import FunctionDispatcher, KeyType

__all__ = ("multimethod", "has_multimethods")

C = TypeVar("C")
T = TypeVar("T", bound=Union[Callable[..., Any], type])


def multimethod(*argtypes: KeyType) -> Callable[[T], MethodDispatcher[T]]:
    """Declare method as multimethod.

    This decorator works exactly the same as :func:`.multidispatch` decorator
    but replaces decorated method with :class:`.MethodDispatcher` object
    instead.

    Should be used only for decorating methods and enclosing class should have
    :func:`.has_multimethods` decorator.
    """

    def _replace_with_dispatcher(func):
        nonlocal argtypes
        argspec = inspect.getfullargspec(func)

        dispatcher = cast(
            MethodDispatcher,
            functools.update_wrapper(
                MethodDispatcher(argspec, len(argtypes) + 1), func
            ),
        )
        dispatcher.register_unbound_rule(func, *argtypes)
        return dispatcher

    return _replace_with_dispatcher


def has_multimethods(cls: type[C]) -> type[C]:
    """Declare class as one that have multimethods.

    Should only be used for decorating classes which have methods decorated with
    :func:`.multimethod` decorator.
    """
    for name, obj in cls.__dict__.items():
        if isinstance(obj, MethodDispatcher):
            obj.proceed_unbound_rules(cls)
    return cls


class MethodDispatcher(FunctionDispatcher[T]):
    """Multiple dispatch for methods.

    This object dispatch call to method by its class and arguments types.
    Usually it is produced by :func:`.multimethod` decorator.

    You should not manually create objects of this type.
    """

    def __init__(self, argspec: inspect.FullArgSpec, params_arity: int) -> None:
        super().__init__(argspec, params_arity)

        # some data, that should be local to thread of execution
        self.local = threading.local()
        self.local.unbound_rules = []

    def register_unbound_rule(self, func, *argtypes) -> None:
        """Register unbound rule that should be processed by
        ``proceed_unbound_rules`` later."""
        self.local.unbound_rules.append((argtypes, func))

    def proceed_unbound_rules(self, cls) -> None:
        """Process all unbound rule by binding them to ``cls`` type."""
        for argtypes, func in self.local.unbound_rules:
            argtypes = (cls,) + argtypes
            print("register rule", argtypes)
            self.register_rule(func, *argtypes)
        self.local.unbound_rules = []

    def __get__(self, obj, cls):
        return self if obj is None else types.MethodType(self, obj)

    def register(self, *argtypes: KeyType) -> Callable[[T], T]:
        """Register new case for multimethod for ``argtypes``"""

        def make_declaration(meth):
            self.register_unbound_rule(meth, *argtypes)
            return self

        return make_declaration

    @property
    def otherwise(self) -> Callable[[T], T]:
        """Decorator which registers "catch-all" case for multimethod."""

        def make_declaration(meth):
            self.register_unbound_rule(meth, *([object] * (self.params_arity - 1)))
            return self

        return make_declaration
