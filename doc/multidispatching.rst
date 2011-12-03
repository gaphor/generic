Multidispatching
================

Multidispatching is a way of implementing `subtype polymorphism`_ in programming
languages. Python already has subtype polymorphism in form of methods on classes
-- you can define different implementations of single method on different
classes then calling such method would execute different implementation based on
type of object you call this method on.

Generic provides another way of implementing subtype polymorphism in Python --
multidispatching in form of *multifunctions* and *multimethods*. All
functionality is provided via ``generic.multidispatch`` module.

.. contents::
   :local:

.. _subtype polymorphism: http://en.wikipedia.org/wiki/Subtype_polymorphism

Multifunctions
--------------

Suppose we want to define a function which behaves differently based on
arguments' types. The naive solution is to inspect argument types with
``isinstance`` function calls but generic provides us with ``@multifunction``
decorator which can easily reduce the amount of boilerplate code and provide
desired level of extensibility::

  from generic.multidispatching import multifunction

  @multifunction(Dog)
  def sound(o):
    print "Woof!"

  @sound.when(Cat)
  def sound(o):
    print "Meow!"

Each separate definition of ``sound`` function works for different argument
types, we will call each such definition *a multifunction case* or simply *a
case*. We can test if our ``sound`` multifunction works as expected::

  >>> sound(Dog())
  Woof!
  >>> sound(Cat())
  Meow!
  >>> sound(Duck())
  Traceback
  ...
  TypeError

The main advantage of using multifunctions over single function with a bunch of
``isinstance`` checks is extensibility -- you can add more cases for other types
even in separate module::

  from somemodule import sound

  @sound.when
  def sound(o)
    print "Quack!"

When behaviour of multifunction depends on some argument we will say that this
multifunction *dispatches* on this argument.

Multifunctions of several arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also have multifunctions of several arguments and even decide on
which of the first arguments you want to dispatch. For example the following
function will only dispatch on its first argument while requiring both of them::

  @multifunction(Dog)
  def walk(dog, meters):
    print "Dog walks for %d meters" % meters

But sometimes you want multifunctions to dispatch on more than one argument, the
you just have to provide several arguments to ``multifunction`` decorator and to
subsequent ``when`` decorators::

  @multifunction(Dog, Cat)
  def is_chases(dog, cat):
    return True

  @is_chases.when(Dog, Dog)
  def is_chases(dog, dog):
    return None

  @is_chases.when(Cat, Dog)
  def is_chases(cat, dog):
    return False

You can have any number of arguments to dispatch on but they should be all
positional, keyword arguments are allowed for multifunctions only if they're not
used for dispatch.

Providing "catch-all" case
~~~~~~~~~~~~~~~~~~~~~~~~~~

There should be an analog to ``else`` statement -- a case which is used when no
matching case is found, we will call such case *a catch-all case*, here is how
you can define it using ``otherwise`` decorator::

  @sound.otherwise
  def sound(o):
    print "<unknown>"

You can try calling ``sound`` with whatever argument type you wish, it will
never fall with ``TypeError`` anymore.

Multimethods
------------

Another functionality provided by ``generic.multidispatch`` module are
*multimethods*. Multimethods are similar to multifunctions except they are...
methods. Technically the main and the only difference between multifunctions and
multimethods is the latter is also dispatch on ``self`` argument.

Implementing multimethods is similar to implementing multifunctions, you just
have to decorate your methods with ``multimethod`` decorator instead of
``multifunction``.  But there's some issue with how Python's classes works which
forces us to use also ``has_multimethods`` class decorator::

  from generic.multidispatch import multimethod, has_multimethods

  @has_multimethods
  class Animal(object):

    @multimethod(Vegetable)
    def can_eat(self, food):
      return True

    @can_eat.when(Meat)
    def can_eat(self, food):
      return False

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

  @has_multimethods
  class Predator(Animal):

    @Animal.can_eat.when(Meat)
    def can_eat(self, food):
      return True

This will redefine ``can_eat`` method on ``Predator`` instances but the *only*
for case for ``Meat`` argument, we can check if with ``Vegetable`` behaviour is
the same::

  >>> predator = Predator()
  >>> predator.can_eat(Vegetable())
  True
  >>> predator.can_eat(Meat())
  True

The only thing to care is you should not forget to include ``@has_multimethods``
decorator on classes which define or override multimethods.

API reference
-------------

.. autofunction:: generic.multidispatch.multifunction

.. autofunction:: generic.multidispatch.multimethod

.. autofunction:: generic.multidispatch.has_multimethods

.. autoclass:: generic.multidispatch.FunctionDispatcher
   :members: when, override, otherwise

.. autoclass:: generic.multidispatch.MethodDispatcher
   :members: when, override, otherwise
