"""Registry.

This implementation was borrowed from happy[1] project by Chris Rossi.

[1]: http://bitbucket.org/chrisrossi/happy
"""

from __future__ import annotations

from typing import Any, Dict, Generator, Generic, KeysView, Sequence, TypeVar, Union

__all__ = ("Registry", "SimpleAxis", "TypeAxis")

K = TypeVar("K")
S = TypeVar("S")
T = TypeVar("T")
V = TypeVar("V")
Axis = Union["SimpleAxis", "TypeAxis"]


class Registry(Generic[T]):
    """Registry implementation."""

    def __init__(self, *axes: tuple[str, Axis]):
        self._tree: _TreeNode[T] = _TreeNode()
        self._axes = [axis for name, axis in axes]
        self._axes_dict = {name: (i, axis) for i, (name, axis) in enumerate(axes)}

    def register(self, target: T, *arg_keys: K, **kw_keys: K) -> None:
        tree_node = self._tree
        for key in self._align_with_axes(arg_keys, kw_keys):
            tree_node = tree_node.setdefault(key, _TreeNode())

        if tree_node.target is not None:
            raise ValueError(
                f"Registration for {target} conflicts with existing registration {tree_node.target}."
            )

        tree_node.target = target

    def get_registration(self, *arg_keys: K, **kw_keys: K) -> T | None:
        tree_node = self._tree
        for key in self._align_with_axes(arg_keys, kw_keys):
            if key not in tree_node:
                return None
            tree_node = tree_node[key]

        return tree_node.target

    def lookup(self, *arg_objs: V, **kw_objs: V) -> T | None:
        return next(self.query(*arg_objs, **kw_objs), None)

    def query(self, *arg_objs: V, **kw_objs: V) -> Generator[T | None, None, None]:
        objs = self._align_with_axes(arg_objs, kw_objs)
        axes = self._axes
        return self._query(self._tree, objs, axes)

    def _query(
        self, tree_node: _TreeNode[T], objs: Sequence[V | None], axes: Sequence[Axis]
    ) -> Generator[T | None, None, None]:
        """Recursively traverse registration tree, from left to right, most
        specific to least specific, returning the first target found on a
        matching node."""
        if not objs:
            yield tree_node.target
        else:
            obj = objs[0]

            # Skip non-participating nodes
            if obj is None:
                next_node: _TreeNode[T] | None = tree_node.get(None, None)
                if next_node is not None:
                    yield from self._query(next_node, objs[1:], axes[1:])
            else:
                # Get matches on this axis and iterate from most to least specific
                axis = axes[0]
                for match_key in axis.matches(obj, tree_node.keys()):
                    yield from self._query(tree_node[match_key], objs[1:], axes[1:])

    def _align_with_axes(
        self, args: Sequence[S], kw: dict[str, S]
    ) -> Sequence[S | None]:
        """Create a list matching up all args and kwargs with their
        corresponding axes, in order, using ``None`` as a placeholder for
        skipped axes."""
        axes_dict = self._axes_dict
        aligned: list[S | None] = [None for _ in range(len(axes_dict))]

        args_len = len(args)
        if args_len + len(kw) > len(aligned):
            raise ValueError("Cannot have more arguments than axes.")

        for i, arg in enumerate(args):
            aligned[i] = arg

        for k, v in kw.items():
            i_axis = axes_dict.get(k, None)
            if i_axis is None:
                raise ValueError(f"No axis with name: {k}")

            i, axis = i_axis
            if aligned[i] is not None:
                raise ValueError(
                    "Axis defined twice between positional and keyword arguments"
                )

            aligned[i] = v

        # Trim empty tail nodes for faster look-ups
        while aligned and aligned[-1] is None:
            del aligned[-1]

        return aligned


class _TreeNode(Generic[T], Dict[Any, Any]):
    target: T | None = None

    def __str__(self) -> str:
        return f"<TreeNode {self.target} {dict.__str__(self)}>"


class SimpleAxis:
    """A simple axis where the key into the axis is the same as the object to
    be matched (aka the identity axis). This axis behaves just like a
    dictionary.  You might use this axis if you are interested in registering
    something by name, where you're registering an object with the string that
    is the name and then using the name to look it up again later.

    Subclasses can override the ``get_keys`` method for implementing
    arbitrary axes.
    """

    def matches(
        self, obj: object, keys: KeysView[object | None]
    ) -> Generator[object, None, None]:
        for key in [obj]:
            if key in keys:
                yield obj


class TypeAxis:
    """An axis which matches the class and super classes of an object in method
    resolution order."""

    def matches(
        self, obj: object, keys: KeysView[type | None]
    ) -> Generator[type, None, None]:
        for key in type(obj).mro():
            if key in keys:
                yield key
