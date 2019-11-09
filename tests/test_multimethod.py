import pytest

from generic.multimethod import has_multimethods, multimethod


def test_multimethod():
    @has_multimethods
    class Dummy(object):
        @multimethod(int)
        def foo(self, x):
            return x + 1

        @foo.register(str)  # type: ignore[no-redef]
        def foo(self, x):
            return x + "1"

    assert Dummy().foo(1) == 2
    assert Dummy().foo("1") == "11"
    with pytest.raises(TypeError):
        Dummy().foo([])


def test_multimethod_with_two_arguments():
    @has_multimethods
    class Dummy(object):
        @multimethod(int, int)
        def foo(self, x, y):
            return x * y

        @foo.register(str, int)  # type: ignore[no-redef]
        def foo(self, s, x):
            return s * x

    assert Dummy().foo(1, 1) == 1
    assert Dummy().foo("1", 2) == "11"
    with pytest.raises(TypeError):
        Dummy().foo([])


def test_multimethod_otherwise_clause():
    @has_multimethods
    class Dummy(object):
        @multimethod(int)
        def foo(self, x):
            return x + 1

        @foo.otherwise  # type: ignore[no-redef]
        def foo(self, x):
            return type(x)

    assert Dummy().foo(1) == 2
    assert Dummy().foo("") is str
    assert Dummy().foo([]) is list


def test_multimethod_otherwise_clausewith_two_arguments():
    @has_multimethods
    class Dummy(object):
        @multimethod(int, int)
        def foo(self, x, y):
            return x * y

        @foo.otherwise  # type: ignore[no-redef]
        def foo(self, s, x):
            return f"{s} {x}"

    assert Dummy().foo(1, 2) == 2
    assert Dummy().foo("a", []) == "a []"


def test_inheritance():
    @has_multimethods
    class Dummy(object):
        @multimethod(int)
        def foo(self, x):
            return x + 1

        @foo.register(float)  # type: ignore[no-redef]
        def foo(self, x):
            return x + 1.5

    @has_multimethods
    class DummySub(Dummy):
        @Dummy.foo.register(str)
        def foo(self, x):
            return x + "1"

        @foo.register(tuple)  # type: ignore[no-redef]
        def foo(self, x):
            return x + (1,)

        @Dummy.foo.register(bool)  # type: ignore[no-redef]
        def foo(self, x):
            return not x

    assert Dummy().foo(1) == 2
    assert Dummy().foo(1.5) == 3.0

    with pytest.raises(TypeError):
        Dummy().foo("1")
    assert DummySub().foo(1) == 2
    assert DummySub().foo(1.5) == 3.0
    assert DummySub().foo("1") == "11"
    assert DummySub().foo((1, 2)) == (1, 2, 1)
    assert DummySub().foo(True) == False
    with pytest.raises(TypeError):
        DummySub().foo([])


def test_override_in_same_class_not_allowed():
    with pytest.raises(ValueError):

        @has_multimethods
        class Dummy(object):
            @multimethod(str, str)
            def foo(self, x, y):
                return x + y

            @foo.register(str, str)  # type: ignore[no-redef]
            def foo(self, x, y):
                return y + x


def test_inheritance_override():
    @has_multimethods
    class Dummy(object):
        @multimethod(int)
        def foo(self, x):
            return x + 1

    @has_multimethods
    class DummySub(Dummy):
        @Dummy.foo.register(int)
        def foo(self, x):
            return x + 3

    assert Dummy().foo(1) == 2
    assert DummySub().foo(1) == 4
