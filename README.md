# Generic programming library for Python

[![Build state](https://github.com/gaphor/generic/workflows/build/badge.svg)](https://github.com/gaphor/generic/actions)
[![Maintainability](https://qlty.sh/gh/gaphor/projects/generic/maintainability.svg)](https://qlty.sh/gh/gaphor/projects/generic)
[![Code Coverage](https://qlty.sh/gh/gaphor/projects/generic/coverage.svg)](https://qlty.sh/gh/gaphor/projects/generic)
[![Documentation Status](https://readthedocs.org/projects/generic/badge/?version=latest)](https://generic.readthedocs.io/en/latest/?badge=latest)
[![Matrix](https://img.shields.io/badge/chat-on%20Matrix-success)](https://app.element.io/#/room/#gaphor_Lobby:gitter.im)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/gaphor/generic/badge)](https://securityscorecards.dev/viewer/?platform=github.com&org=gaphor&repo=generic)

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

## 1.1.6

- Refactoring

## 1.1.5

- Fix regression with super type dispatching
- Dependency updates

## 1.1.4

- Dependency updates

## 1.1.3

- Dependency updates

## 1.1.2

- Replace print statements with logging
- Enable trusted publisher for PyPI
- Create Security Policy
- Update LICENSE to BSD 3-Clause
- Add support for Python 3.12
- Simplify build: drop tox
- Update documentation theme to Furo
- Switch linting to ruff

## 1.1.1

- Add support for Python 3.11
- Move mypy configuration to pyproject.toml
- Enable automatic release of new versions with CI

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
