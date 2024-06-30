from __future__ import annotations

from sys import version_info
from typing import Callable

import pytest
if version_info < (3, 11):
    from exceptiongroup import ExceptionGroup

from generic.event import Event, Manager


@pytest.fixture
def events():
    return Manager()


def make_handler(effect: object) -> Callable[[Event], None]:
    def handler(e):
        e.effects.append(effect)
        raise ValueError(effect)

    return handler


def test_handle_all_subscribers(events):
    events.subscribe(make_handler("handler1"), MyEvent)
    events.subscribe(make_handler("handler2"), MyEvent)
    e = MyEvent()
    with pytest.raises(ExceptionGroup):
        events.handle(e)

    assert len(e.effects) == 2
    assert "handler1" in e.effects
    assert "handler2" in e.effects


def test_collect_all_exceptions(events):
    events.subscribe(make_handler("handler1"), MyEvent)
    events.subscribe(make_handler("handler2"), MyEvent)
    e = MyEvent()
    with pytest.raises(ExceptionGroup) as excinfo:
        events.handle(e)

    exc = excinfo.value
    nested_exc = [str(e) for e in exc.exceptions]
    assert len(exc.exceptions) == 2
    assert "handler1" in nested_exc
    assert "handler2" in nested_exc


class MyEvent:
    def __init__(self) -> None:
        self.effects: list[object] = []
