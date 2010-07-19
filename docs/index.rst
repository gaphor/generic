.. generic documentation master file, created by
   sphinx-quickstart on Mon Jul 19 01:35:17 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Generic documentation
================================

.. toctree::
   :maxdepth: 2

Generic is a programming library for Python that provides tools for generic
programming. By, now there is only one feature -- multiple dispatch.

Multiple dispatch
-----------------

Multiple dispatch (or multidispatch) is a technique of choosing the function
implementation at runtime based on its argument types. For illustrating the
problem, let's see example function that behaves differently when you provide
it ``str`` or ``int`` object as argument::

    def add_two(x):
        if isinstance(x, int):
            return add_two_int(x)
        elif isinstance(x, str):
            return add_two_str(x)
        else:
            raise TypeError("Wrong argument type.")

    def add_two_int(x):
        return x + 2

    def add_two_str(x):
        return x + "2"

    assert add_two(2) == 4
    assert add_two("2") == "22"

The last two assertions are true -- the function ``add_two`` dispatches their
execution either to ``add_two_int`` or ``add_two_str`` depending on its
argument type. As for me, this piece of code is very verbose and unpythonic.
This is there ``generic.multidispatch`` comes in place.


Declaring multifunctions
~~~~~~~~~~~~~~~~~~~~~~~~

With help of ``generic.multidispatch`` module we can rewrite the latter
piece of code like that::

    from generic.multidispatch import multifunction

    @multifunction(int)
    def add_two(x):
        return x + 2

    @add_two.when(str)
    def add_two(x):
        return x + "2"

    assert add_two(2) == 4
    assert add_two("2") == "22"

And again -- assertions are fulfilled, but now code is more readable and
declarative.

Furthermore, this way of writing functions is more extensible, because we can
add another branch (another implementation for some other argument type) to our
function ``add_two`` by being able not to modify original declarations, even if
they are defined in another module or package::

    from mymodule import add_two

    @add_two.when(list)
    def add_two(x):
        return x + [2]

Doing the same thing for function from first example would require modify
function code for each type we want to handle, which isn't good.


Overriding multifunction implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're trying to define multifunction implementation for types, that already have another implementation, then ``TypeError`` exception would be raised. But there is a way to do this kind of things in explicitly manner::
    
    @add_two.override(list)
    def add_two(x):
        return x + [2, 2]

Note the using of the ``@add_two.override`` decorator instead of the
``@add_two.when`` one.


Multifunctions with more than one arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example from the previous section demonstrates basic usage of
``generic.multidispatch`` for defining multifunctions with single argument.
Now, let's see how we can define multifunctions with more than one arguments::

    @multifunction(int, int)
    def add(x, y):
        return x + y

    @add.when(str, str)
    def add(x, y):
        return add(int(x), int(y))

This is as simple as it can be -- just pass more types to ``multifunction``
decorator to produce multifunction that dispatches by exactly that number of
arguments.

If function takes more arguments than the number of types you have passed to
``multifunction`` decorator, they will be treated as typical arguments and
there will be no dispatching by them. The same holds for keyword and variable
(prefixed with ``*`` or ``**``) arguments.

The only requirements for declaring multifunctions are:

* The number of function's positional arguments should not be less than the
  number of types passed to ``multifunction`` decorator. This is because
  dispatching is allowed only by positional arguments.

* All function implementations that are related to one multifunction should
  have the same arity for positional arguments.


Declaring multimethods
~~~~~~~~~~~~~~~~~~~~~~

*Generic* can help with defining multifunctions, but what about methods? There
are another decorators for them::

    from generic.multidispatch import multimethod
    from generic.multidispatch import has_multimethods

    @has_multimethods
    class A(object):

        @multimethod(int)
        def foo(self, x):
            return x + 1

        @foo.when(str)
        def foo(self, x):
            return x + "1"

    assert A().foo(1) == 2
    assert A().foo("1") == "11"

It may seen works exactly like multifunctions, but it's not. The main
difference between multifunctions and multimethods is that the latter is
dispatched also by its class type. This is why we need another decorator
``has_multimethods`` for classes that define multimethods.

.. warning::
    Decorating class with ``has_multimethods`` decorator is mandatory to
    multimethods declaration to work. This is because we cannot know method's
    class at the time of method declaration.

Let's see example demonstrates usage of that feature::

    @has_multimethods
    class B(A):

        @A.foo.when(list)
        def foo(self, x):
            return x + [1]

    assert B().foo(1) == 2
    assert B().foo("1") == "11"
    assert B().foo([1]) == [1, 1]

As you can see, we have extended method ``foo`` inherits all previous
declarations, but also adds another one -- for ``list`` type. Note, that declaration is only works for ``B`` objects, but not for ``A`` ones::

    A().foo([1]) # bad! raises TypeError


Also, note, that all multimethods declarations are overridden implicitly, so
the ``A.foo.override`` and ``A.foo.when`` decorators are the same.

All other things that are true for multifunctions are also hold for
multimethods.

Development
-----------

Development of *generic* library takes place at `github
<http://github.com/andreypopp/generic>`_ -- there are code repository and issue
tracker.

API referrence
--------------

.. autofunction:: generic.multidispatch.multifunction

.. autofunction:: generic.multidispatch.multimethod

.. autofunction:: generic.multidispatch.has_multimethods

.. autoclass:: generic.multidispatch.FunctionDispatcher

.. autoclass:: generic.multidispatch.MethodDispatcher

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

