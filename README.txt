Goal and usage
==============

Add collective.noindexing to the eggs in your buildout (and to zcml on
Plone 3.2 or earlier).  On Zope instance startup this will patch some
catalog methods so no indexing, reindexing or unindexing is done at
all.  The idea is that you use this package temporarily so you can
quickly move a big part of your Plone Site to a different folder
without having to worry about indexing.  It really makes moving a lot
faster.  You do the indexing later, probably by doing a catalog clear
and rebuild; you have a bit more control there about subtransactions,
to help avoid a ``MemoryError`` or ``[Errno 24] Too many open files``.


Alternatives
------------

- Go to the ``archetype_tool`` object in the ZMI, and then to the
  Catalogs tab.  Switching off ``portal_catalog`` there should have
  the same effect.

- Add ``Products.QueueCatalog`` and ``Products.PloneQueueCatalog`` to
  the eggs of your buildout.  In the ``portal_quickinstaller`` install
  PloneQueueCatalog.  This renames the ``portal_catalog`` to
  ``portal_catalog_real`` and creates a ZCatalog Queue with the id
  ``portal_catalog``.  The standard settings worked fine for me.  You
  now do that large move.  In the fresh ``portal_catalog`` you go to
  the Queue tab.  It should say you have lots of items in the queue,
  in my case around 12,000.  Clicking the 'Process Queue' button will
  by default process just twenty items of that queue.  You can
  increase that number.  This is an easy way of avoiding MemoryErrors
  during indexing, as the total number of objects reindexed in one go
  will be as low as you want.

I (Maurits) went for the PloneQueueCatalog solution.  But I wrote this
``collective.noindexing`` package already, nicking some code from
``collective.indexing`` and it also worked, so I thought I might as
well at least put the code in the collective.  Bug me if you want a
release.


To Do
-----

- Maybe don't do any patching by default, but make one or two browser
  views so you can switch the patches on and off, without having to
  remove the package from the eggs again to return to normal
  behaviour.


Maurits van Rees
