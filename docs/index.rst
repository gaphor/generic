.. generic documentation master file, created by
   sphinx-quickstart on Sun Jun 26 12:37:44 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Generic 0.3 documentation
=========================

Generic is a general purpose programming library aminig to bring some of the
generic and reusable programming features to Python.

.. contents:: Documentation contents

Overview and installation instructions
--------------------------------------

Generic is trying to be simple and easy-to-use programming library that provides
a core set of tools for generic programming in Python. It has no external
dependencies. It is very small and trying to be well documented and tested.

The installation process is quite simple, you can just use *easy_install*::

  easy_install generic

or *pip*:: 

  pip install generic

Recent in-development version of library is hosted on the *GitHub*, so you can clone the repo with::

  git clone http://github.com/andreypopp/generic

Multidispatching
----------------

Multidispatching is not a new concept in the world of programming languages --
it's well known in the various LISPs dialects and more recenlty -- from Clojure,
which is exactly LISP but on JVM.

Multidispatching is a some kind of control structure for dispatching function
call into separate code branches based on function argument values. The basic
and naive implementation of such technique can be written as::

    def double(x):
      if isinstance(x, int):
        return double_int(x)
      elif isinstance(x, basestring):
        return double_basestring(x)
      else:
        raise TypeError()

    def double_int(x):
      return x * 2

    def double_basestring(x):
      return str(int(x) * 2)

    assert double(2) == 4
    assert double("2") == "4"

So the ``double`` function just inspects its argument type and dispatch
execution to ``double_int`` or ``double_basestring`` by situation. We will call
such functions *multifunctions*. Note, that this technique can be also applied
to functions of multiple arguments or you can define methods as multifunctions
(in this case we will call them *multimethods*).

The approach above works but it has some drawbacks:

  * It requires too much boilerplate -- it is really boring to write down all
    these ``isinstance`` checks by hand.

  * It provides no extensibility -- you (or other developer) cannot manage
    ``double`` function to handle more types than ``basestring`` or ``int`` by
    not modifying original source code of ``double`` function.

Generic is targeting at providing another way to define multifunctions and
multimethods which are not affected by these issues.

Multifunctions
~~~~~~~~~~~~~~

Let's see how we can rewrite our ``double`` multifunction with help of generic
library::

  from generic.multidispatch import multifunction

  @multifunction(int)
  def double(x):
    returx x * 2

  @double.when(basestring)
  def double(x):
    return str(int(x) * 2)

  assert double(2) == 4
  assert double("2") == "4"

As you can see generic takes care of all dispatching logic providing simple
decorator-based interface for defining multifunctions. 

By using generic's multifunctions you can also extend your multifunctions from
another modules::

  # Another module
  from yourapp import double

  @double.when(bool)
  def double(x):
    return bool(int(x) * 2)

  assert double(2) == 4
  assert double("2") == "4"
  assert double(True) == True

So you can use that approach for application extensibilty by wrapping
functionality to be extended by 3rd party software into multifunctions.

Multimethods
~~~~~~~~~~~~

Multimethods are the same for methods as multifunctions for functions --
they provide dispatching mechanism based on argument types (also on ``self``).

Let's define multimethod with generic::

  from generic.multidispatch import multimethod, has_multimethods

  @has_multimethods
  class MyClass(object):

    @multimethod
    def double(self, x):
      return x * 2

    @double.when(basestring)
    def double(self, x):
      return str(int(x) * 2)

  o = MyClass()
  assert o.double(2) == 4
  assert o.double("2") == "4"

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

