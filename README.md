# Generic programming library for Python

[![Build state](https://github.com/gaphor/generic/workflows/build/badge.svg)](https://github.com/gaphor/generic/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7be2d28400687b1375a/maintainability)](https://codeclimate.com/github/gaphor/generic/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c7be2d28400687b1375a/test_coverage)](https://codeclimate.com/github/gaphor/generic/test_coverage)
[![Documentation Status](https://readthedocs.org/projects/generic/badge/?version=latest)](https://generic.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/Gaphor/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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

## 1.1.0

- Rename `master` branch to `main`
- `generic.event.Manager` executes all handlers and throws an `ExceptionGroup` in case of errors

## 1.0.1

- Add Support for Python 3.10, Drop Support for Python 3.7
- Enable Pre-commit Hooks for isort, toml, yaml, pyupgrade, docformatter, and flake8
- Migrate to GitHub Actions

## 1.0.0

- Updated documentation on [Readthedocs](https://generic.readthedocs.io)
- Fix `multimethod.otherwise` clause

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
