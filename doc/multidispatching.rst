Multidispatching
================

Multidispatching is a way of implementing `subtype polymorphism`_ in programming
languages. Python already has subtype polymorphism in form of methods on classes
-- you can define different implementations of single method on different
classes then calling such method would execute different implementation based on
type of object you call this method on.

Generic provides another way of implementing subtype polymorphism in Python --
multidispatching in form of *multifunctions* and *multimethods*.

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

This works as expected::

  >>> sound(Dog())
  Woof!
  >>> sound(Cat())
  Meow!

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

You can also have multifunctions of several arguments, you can even decide on
which of the first arguments you want to dispatch. For example the following function
will only dispatch on its first argument while requiring both of them::

  @multifunction(Dog)
  def walk(dog, meters):
    print "Dog walks for %d meters" % meters

Next example demonstrates multifunction which dispatches on its both arguments::

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

Multimethods
------------

Multidispatching vs. subclassing
--------------------------------

.. _subtype polymorphism: http://en.wikipedia.org/wiki/Subtype_polymorphism
