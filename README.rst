Generic programming library for Python
======================================

Generic is trying to be simple and easy-to-use programming library that
features the following:

* Multidispatching mechanisms for functions and methods (latter is not
  implemented yet).
* Registries with different and user-defined lookup strategies.
* Event system (not implemented).

Its development takes place at http://github.com/andreypopp.

Multidispatching
----------------

Generic library provides way to define function with multidispatching feature::

    from generic.multidispatching import multifunction

    @multifunction(int, int)
    def add(x, y):
        return x + y

    @add.when(str, str)
    def add(x, y):
        return add(int(x), int(y))

And then in console::

    >>> add(1, 2)
    3
    >>> add("1", "2")
    3
    >>> add("1", 2)
    Traceback
    ...
    TypeError: ...
