# -*- coding: utf-8 -*-
"""paved -- common paver tasks.

Copyright 2010 David Eyk. All rights reserved.
"""
from paver.easy import *

import urllib


__cwd__ = path('.').abspath()

options(
    paved = Bunch(
        distribute_url = "http://python-distribute.org/distribute_setup.py",
        cwd = __cwd__,
        clean_patterns = ["*.pyc", "*~", "*.pyo", "*#", ".#*", "*.lock", "*.log*"],
        clean_dirs = [__cwd__]
        )
    )


@task
def get_distribute(options):
    """Retrieve a copy of distribute_setup.py for distribution.
    """
    url = urllib.urlopen(options.paved.distribute_url)
    with open(options.paved.cwd / 'distribute_setup.py', 'w') as fo:
        fo.write(url.read())


@task
def clean(options):
    """Clean up.

    options.paved.clean_dirs: directories to search recursively
    options.paved.clean_patterns: patterns to search for and remove
    """
    for wd in options.paved.clean_dirs:
        print "Cleaning", wd
        for p in options.paved.clean_patterns:
            for f in wd.walkfiles(p):
                f.remove()


@task
@consume_args
def pip_install(args):
    sh('pip install %s' % (' '.join(args)))


@task
@consume_args
def easy_install(args):
    sh('easy_install %s' % (' '.join(args)))
