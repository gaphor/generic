# Generic programming library for Python

Generic is a library for [Generic programming](https://en.wikipedia.org/wiki/Generic_programming), also known as [Multiple dispatch](https://en.wikipedia.org/wiki/Multiple_dispatch).

The Generic library supports:

* multi-dispatch: like `functools.singledispatch`, but for more than one parameter
* multi-methods: multi-dispatch, but for methods
* event dispatching: based on a hierarchical event structure (event objects)

You can read
[documentation](http://generic.readthedocs.org/en/latest/index.html) hosted at
excellent readthedocs.org project. Development takes place on
[github](http://github.com/gaphor/generic).


# Changes

## 1.0.0b1

- Ported the code to Python 3.7, Python 2 is no longer supported
- Multimethods now have their own module
- The interface now mimics `functools.singledispatch`:
  - the `when` method has been renamed to `register`
  - overriding of methods is no longer possible

## 0.3.1

- Minor fixes in distribution.

## 0.3

- Event management with event inheritance support.

## 0.2

- Methods with multidispatch by object type and positional arguments.
- Override multifunctions with ``override`` method.

## 0.1

- Registry with simple and type axes.
- Functions with multidispatch by positional arguments.
