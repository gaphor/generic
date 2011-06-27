.. generic documentation master file, created by
   sphinx-quickstart on Sun Jun 26 12:37:44 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Generic 0.3 documentation
=========================

Generic is a general purpose programming library aminig to bring some of the
generic and reusable programming features to Python.

.. contents:: Documentation contents
   :local:
   :backlinks: none

Overview
--------

Generic is trying to be simple and easy-to-use programming library that provides
a core set of tools for generic programming in Python by being as much
"pythonic" as possible. It has no external dependencies, it is very small and
trying to be well documented and tested.

Installation and development process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The installation process is quite simple, you can just use ``easy_install
generic`` or ``pip install generic`` command to obtain the most recent stable
version of library.

Recent in-development version of library is hosted_ on the *GitHub*, so you can clone the repo with::

  git clone http://github.com/andreypopp/generic

For reporting bugs you can use issues_ on GitHub.

.. _issues: https://github.com/andreypopp/generic/issues
.. _hosted: https://github.com/andreypopp/generic

What's in 0.3 version
~~~~~~~~~~~~~~~~~~~~~

Generic 0.3 is the first more or less public and usable release, it contains:

* Registry implementation borrowed from happy_ project by Chris Rossi.

* Event management API with event inheritance support.

* Multidispatching with functions and methods.


See changelog_ for more details.

.. _happy: https://bitbucket.org/chrisrossi/happy
.. _changelog: https://github.com/andreypopp/generic/blob/master/CHANGELOG.rst

Similar projects
~~~~~~~~~~~~~~~~

Multidispatching
----------------

Multidispatching is a technique of providing different code implementations for
different data behind the simple and uniform interface. Let's better
provide example of such approach::

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

The ``double`` function just inspects its argument type and dispatch
execution to ``double_int`` or ``double_basestring`` by situation. Such function is called *multifunction* and other two -- *concrete implementations*.

.. sidebar:: A bit of history
   
   Multidispatching is not a new concept in the world of programming languages
   -- it's well known in the LISP world. The most recent implementation of LISP
   on JVM -- Clojure -- also provides such feature.

But what's wrong with the example above? Why generic is trying to provide
another way to define multifunctions (and *multimethods*) in Python?

There're two issues which are not addressed by this naive implementation --
*simplicity* and *extensibity*.

Let's see again at the ``double`` function -- it just consist of a bunch of
conditional statements with ``isinstance`` checks. Writing them down by hand is
cumbersome, it should be generated automatically from some declarations.

Speaking of extensibily -- ``double`` function cannot be extended to handle more
argument types by not modifying its source code, which isn't a good thing.

Generic is trying to address these issues by providing a declarative way for
defining multifunctions and multimethods.

Multifunctions
~~~~~~~~~~~~~~

Let's see how we can rewrite our ``double`` multifunction with help of generic
library::

  from generic.multidispatch import multifunction

  @multifunction(int)
  def double(x):
    return x * 2

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

Overriding multifunction implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

First of all spot some differences between multimethods and multifunctions --
we're using ``multimethod`` decorator and decorating enclosed class with
``has_multimethods`` class-decorator. The later is becuase of Python object
model -- we cannot inject attributes inside class while the class is being
constructed. 

.. sidebar:: Why using class decorator?

   We need to convert our multimethods instances into UnboundMethod objects
   after the class is constructed -- this is the way CPython, the refercen
   Python implementation, handles class construction.

Apart from that two things there're no other big differences -- multimethods
behave the same. Another fancy thing we can do with multimethods is 

Case study: pretty printing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thread safety
~~~~~~~~~~~~~

Event management
----------------

Another topic generic brings to the table is *event management*, which is the
right tool for building extensible and yet simple pieces of software.

What event management means? It is about

  * Making your application components speak in term of events not direct calls
    into each other.

  * Providing a way to 3rd party developers extend your application by providing
    own event handlers.

It may sounds complex and huge but in its core it is just about events (which
are just plain simple Python objects) and event handlers (which are Python
functions).

Generic provides *global event management API* which is suitable for small and
simple applications and more customized *event management API* (on which global
API is based on) for more complex application.

Global event management API
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's start with the example::

  from generic.event import subscribe, fire

  class PizzaDelivered(object):
    """ Indicates pizza delivered situatuion in your application."""

    def __init__(self, pizza):
      self.pizza = pizza
      self.money = None

    def pay(self, money):
      self.money = money

  @subscribe(PizzaDelivered)
  def pay_bill(event):
    event.pay(25)

  pizza_delivered = PizzaDelivered("4 cheeses")
  assert pizza_delivered.money is None
  fire(pizza_delivered)
  assert not pizza_delivered.money == 25

The last assertion says us that ``pay_bill`` function was executed with
``pizza_delivered`` event object as argument after we've fired it.

As I've mentined previously events allow us to decouple application components
from each other -- we do not call ``pay_bill`` function directly, which is good
thing.

Also we can now extend our pizza-style application by just registering another
handlers::

  # Another module
  from pizzaapp import PizzaDelivered
  from generic.event import subscribe
  from logging import getLogger

  log = getLogger('pizzalogger')

  @subscribe(PizzaDelivered)
  def pizza_logger(event):
    log.info("Pizza '%s' was delivered", event.pizza)

So after ``fire(pizza_delivered)`` call we will see corresponding record in our
log output.

Working with event managers directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes using global API isn't a good thing -- maybe we want to host several
application instances inside one Python interpreter or just to separate
different event types into different event management tiers. Fortunately we can
work with so-called *event managers* directly by creating them and registering
event handlers against them::

  from generic.event import Manager

  events = Manager()

  class Event(object):
    def __init__(self):
      self.processed = False

  @events.subscribe(Event):
  def handle(event):
    event.processed = True

  e = Event()
  assert not e.processed
  events.fire(e)
  assert e.processed

As you can working with manager directly isn't more difficult than working with
global event management API (actually global API implemented as global event
manager object sitting inside of ``generic.event`` module).

You can create as many event managers as you want -- one per thread and store it
in thread-local container or just one per application instance and so on.

Subclassing events
~~~~~~~~~~~~~~~~~~

Case study: processing bank accounts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thread safety
~~~~~~~~~~~~~

What about threadsafety? There're two aspects to discuss here.

Registry
--------

Type axis
~~~~~~~~~

Implementing custom axis
~~~~~~~~~~~~~~~~~~~~~~~~

Case study: HTTP request dispatching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thread safety
~~~~~~~~~~~~~

API reference
-------------

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

