""" Event management system."""

from collections import namedtuple

from generic.registry import Registry
from generic.registry import TypeAxis

__all__ = ["Manager", "subscribe", "unsubscribe", "fire"]


class HandlerSet(namedtuple("HandlerSet", ["parents", "handlers"])):
    """ Set of handlers for specific type of event."""

    @property
    def all_handlers(self):
        """ Iterate over own and supertypes' handlers."""
        seen = set()
        seen_add = seen.add

        # yield own handlers first
        for handler in self.handlers:
            seen_add(handler)
            yield handler

        # yield supertypes' handlers then
        for parent in self.parents:
            for handler in parent.all_handlers:
                if not handler in seen:
                    seen_add(handler)
                    yield handler


class Manager(object):
    """ Event manager."""

    def __init__(self):
        axes = (("event_type", TypeAxis()),)
        self.registry = Registry(*axes)

    def subscribe(self, handler, event_type):
        """ Subscribe ``handler`` to specified ``event_type``."""
        handler_set = self.registry.get_registration(event_type)
        if not handler_set:
            handler_set = self._register_handlers(event_type)
        handler_set.handlers.add(handler)

    def unsubscribe(self, handler, event_type):
        """ Unsubscribe ``handler`` from ``event_type``."""
        handler_set = self.registry.get_registration(event_type)
        if handler_set and handler in handler_set.handlers:
            handler_set.handlers.remove(handler)

    def fire(self, event):
        """ Fire event instance."""
        handler_set = self.registry.lookup(event)
        for handler in handler_set.all_handlers:
            handler(event)

    def _register_handlers(self, event_type):
        """ Derive handlers by copying them for event's subclasses."""
        handlers = set()
        parents = event_type.__bases__
        parent_handler_sets = []
        for parent in parents:
            parent_handlers = self.registry.get_registration(parent)
            if parent_handlers is None:
                parent_handlers = self._register_handlers(parent)
            parent_handler_sets.append(parent_handlers)
        handler_set = HandlerSet(parents=parent_handler_sets, handlers=handlers)
        self.registry.register(handler_set, event_type)
        return handler_set


# Global event manager
_global_manager = Manager()

# Global event management API
subscribe = _global_manager.subscribe
unsubscribe = _global_manager.unsubscribe
fire = _global_manager.fire
