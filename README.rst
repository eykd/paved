=====
Paved
=====

Paved provides common tasks for Paver-based projects.

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

- ``paved.dist``: distribution-related tasks and shortcuts
- ``paved.pkg``: some packaging-related tasks
- ``paved.django``: Django-related tasks
- ``paved.util``: some useful utility functions
- ``paved.util.pycheck``: python code checking functions


Contributing
------------

I'd love to have help with Paved. If you have common tasks that you're
always copying and pasting from one pavement.py to the next, they
probably have a place here. 

The best way to contribute to Paved is to fork the project on Github
and send pull requests to ``eykd``.