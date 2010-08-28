Paved -- common tasks for Paver-based projects
==============================================

Quick Start
-----------

To start using ``paved``, inside your ``pavement.py``::

    from paved import *

This will set up the ``options.paved`` namespace, and give you one
extremely useful task: ``clean``, which takes care of cleaning up common
clutter files like ``*.pyc``, ``*.pyo``, and ``*~``. Of course, it's
customizable using ``options.paved.clean.patterns`` and
``options.paved.clean.dirs``.


Other Modules
-------------

Use the same pattern of ``from paved.<module> import *`` for other
available modules:

- ``paved.pkg``: some packaging-related tasks
- ``paved.django``: Django-related tasks
- ``paved.util``: some useful utility functions
