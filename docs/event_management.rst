Event management
================

Generic library provides :module:`generic.event` for simple event management
with support for event type inheritance. Module API is quite simple -- just one
class :class:`Manager`::

    from generic.event import Manager

    events = Manager()

Now you can use ``events`` to subscribe for events and fire specific event.
Let's see how we can do that.

First of all, we need to define some type of event -- it can be any Python type
you want, for example, user defined class::

    class EntryCreated(object):
        """ Some entry was created."""

        def __init__(self, entry):
            self.entry = entry

Now we define handler for our event ``EntryCreated`` that will print just
created entry on console::

    def print_created_entry(event):
        print "Entry created: %s" % event.entry

    events.subscribe(print_created_entry, EntryCreated)

That's all, now just fire event by creating instance of it and provide it to
``fire`` method::

    events.fire(EntryCreated("new entry")

Now let's subclass ``EntryCreated`` event and specialize it::

    def BlogEntryCreated(EntryCreated):
        """ Blog entry was created."""

Then define event handler for it::

    def print_created_blog_entry(event):
        print "Blog entry created: %s" event.entry

And fire event::

    events.fire(BlogEntryCreated("new blog entry"))

Actually this will print two messages on console, since two event handlers will
be fired -- ``print_created_entry`` and ``print_created_blog_entry``, because
firing ``BlogEntryCreated`` also means firing ``EntryCreated`` (the latter is
superclass of the first one).

There is also ``unsubscribe`` method that allows to unsubscribe specified
handler from specified type of event::

    events.unsubscribe(print_created_entry, EntryCreated)

Now ``print_created_entry`` will no be fired on ``EntryCreated`` event.

Module itself, also provides global API for event management, which is suitable
for small applications, that are not bothering about holding separate event
manager instance::

    from generic.event import subscribe, unsubscribe, fire
