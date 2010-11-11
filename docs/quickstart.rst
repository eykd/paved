==========
Quickstart
==========

Paved comes with several task bundles configured to work out of the
box for the most common use-cases. You use them by importing their
members into your pavement.py's module namespace.

As a quick example, let's start a new Django project. We create our
pavement.py::

    """pavement.py -- paver tasks for our new Django project!
    """
    from paver.easy import *

    __path__ = path(__file__).abspath().dirname()

Now we add these two lines::

    from paved.django import manage

    options.paved.django.manage_py = __path__ / 'myproject' / 'manage.py'

Suddenly, we can start doing things like::

    $ paver manage syncdb

This will run our django project's `manage.py` file with `syncdb` as
the first argument. All of Django's manage commands are available to
us now.

Once we're ready for our first release, having made sure that our
setup() metadata is all there, we add this to the imports::

    from paved.dist import *

Now `sdist` is hooked up as described in Paver's documentation::

    $ paver sdist

This produces a `bootstrap.py`, `setup.py`, `paver-minilib.zip`, as
well as a (configurable) `MANIFEST.in` that does the right stuff by
default. Finally, you'll find your source distribution file in the
`dist/` folder, as you might expect.

Read the :doc:`API documentation </api>` to find out more about the tasks and
utilities available.