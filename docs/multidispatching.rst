Multidispatching
================

Multidispatching allows you to define methods and functions which should behave
differently based on arguments' types without cluttering ``if-elif-else`` chains
and ``isinstance`` calls.

All you need is inside ``generic.multidispatch`` module. See examples below to
learn how to use it to define multifunctions and multimethods.

.. contents::
   :local:

First the basics:

  >>> class Cat: pass
  >>> class Dog: pass
  >>> class Duck: pass

Multifunctions
--------------

Suppose we want to define a function which behaves differently based on
arguments' types. The naive solution is to inspect argument types with
``isinstance`` function calls but generic provides us with ``@multidispatch``
decorator which can easily reduce the amount of boilerplate and provide
desired level of extensibility::

  >>> from generic.multidispatch import multidispatch

  >>> @multidispatch(Dog)
  ... def sound(o):
  ...   print("Woof!")

  >>> @sound.register(Cat)
  ... def cat_sound(o):
  ...   print("Meow!")

Each separate definition of ``sound`` function works for different argument
types, we will call each such definition *a multifunction case* or simply *a
case*. We can test if our ``sound`` multifunction works as expected::

  >>> sound(Dog())
  Woof!
  >>> sound(Cat())
  Meow!
  >>> sound(Duck())  # doctest: +ELLIPSIS
  Traceback (most recent call last):
    ...
  TypeError: No available rule found for ...

The main advantage of using multifunctions over single function with a bunch of
``isinstance`` checks is extensibility -- you can add more cases for other types
even in separate module::

  >>> @sound.register(Duck)
  ... def duck_sound(o):
  ...   print("Quack!")

When behaviour of multifunction depends on some argument we will say that this
multifunction *dispatches* on this argument.

Multifunctions of several arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also define multifunctions of several arguments and even decide on which
of first arguments you want to dispatch. For example the following function will
only dispatch on its first argument while requiring both of them::

  >>> @multidispatch(Dog)
  ... def walk(dog, meters):
  ...   print("Dog walks for %d meters" % meters)

But sometimes you want multifunctions to dispatch on more than one argument,
then you just have to provide several arguments to ``multidispatch`` decorator
and to subsequent ``when`` decorators::

  >>> @multidispatch(Dog, Cat)
  ... def chases(dog, cat):
  ...   return True

  >>> @chases.register(Dog, Dog)
  ... def chases_dog_dog(dog1, dog2):
  ...   return None

  >>> @chases.register(Cat, Dog)
  ... def chases_cat_dog(cat, dog):
  ...   return False

You can have any number of arguments to dispatch on but they should be all
positional, keyword arguments are allowed for multifunctions only if they're not
used for dispatch.

Multimethods
------------

Another functionality provided by ``generic.multimethod`` module are
*multimethods*. Multimethods are similar to multifunctions except they are...
methods. Technically the main and the only difference between multifunctions and
multimethods is the latter is also dispatch on ``self`` argument.

Implementing multimethods is similar to implementing multifunctions, you just
have to decorate your methods with ``multimethod`` decorator instead of
``multidispatch``.  But there's some issue with how Python's classes works which
forces us to use also ``has_multimethods`` class decorator::

  >>> class Vegetable: pass
  >>> class Meat: pass

  >>> from generic.multimethod import multimethod, has_multimethods

  >>> @has_multimethods
  ... class Animal(object):
  ...
  ...   @multimethod(Vegetable)
  ...   def can_eat(self, food):
  ...     return True
  ...
  ...   @can_eat.register(Meat)
  ...   def can_eat(self, food):
  ...     return False
  register rule (<class '__main__.Animal'>, <class '__main__.Vegetable'>)
  register rule (<class '__main__.Animal'>, <class '__main__.Meat'>)

This would work like this::

  >>> animal = Animal()
  >>> animal.can_eat(Vegetable())
  True
  >>> animal.can_eat(Meat())
  False

So far we haven't seen any differences between multifunctions and multimethods
but as it have already been said there's one -- multimethods use ``self``
argument for dispatch. We can see that if we would subclass our ``Animal`` class
and override ``can_eat`` method definition::

  >>> @has_multimethods
  ... class Predator(Animal):
  ...   @Animal.can_eat.register(Meat)
  ...   def can_eat(self, food):
  ...     return True
  register rule (<class '__main__.Predator'>, <class '__main__.Meat'>)

This will override ``can_eat`` on ``Predator`` instances but *only* for the case
for ``Meat`` argument, case for the ``Vegetable`` is not overridden, so class
inherits it from ``Animal``::

  >>> predator = Predator()
  >>> predator.can_eat(Vegetable())
  True
  >>> predator.can_eat(Meat())
  True

The only thing to care is you should not forget to include ``@has_multimethods``
decorator on classes which define or override multimethods.

You can also provide a "catch-all" case for multimethod using ``otherwise``
decorator just like in example for multifunctions.

Providing "catch-all" case
~~~~~~~~~~~~~~~~~~~~~~~~~~

There should be an analog to ``else`` statement -- a case which is used when no
matching case is found, we will call such case *a catch-all case*, here is how
you can define it using ``otherwise`` decorator::

  >>> @has_multimethods
  ... class Animal(object):
  ...
  ...   @multimethod(Vegetable)
  ...   def can_eat(self, food):
  ...     return True
  ...
  ...   @can_eat.register(Meat)
  ...   def can_eat(self, food):
  ...     return False
  ...
  ...   @can_eat.otherwise
  ...   def can_eat(self, food):
  ...     return "?"
  register rule (<class '__main__.Animal'>, <class '__main__.Vegetable'>)
  register rule (<class '__main__.Animal'>, <class '__main__.Meat'>)
  register rule (<class '__main__.Animal'>, <class 'object'>)

  >>> Animal().can_eat(1)
  '?'

You can try calling ``sound`` with whatever argument type you wish, it will
never fall with ``TypeError`` anymore.

API reference
-------------

.. autofunction:: generic.multidispatch.multidispatch

.. autofunction:: generic.multimethod.multimethod

.. autofunction:: generic.multimethod.has_multimethods

.. autoclass:: generic.multidispatch.FunctionDispatcher
   :members: register

.. autoclass:: generic.multimethod.MethodDispatcher
   :members: register, otherwise
