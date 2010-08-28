# -*- coding: utf-8 -*-
"""paved -- common paver tasks.

Copyright 2010 David Eyk. All rights reserved.
"""
from paver.easy import options, path, task
from paver.options import Namespace

from . import util


__cwd__ = path('.').abspath()

options(
    paved = Namespace(
        cwd = __cwd__,
        
        clean = Namespace(
            patterns = ["*.pyc", "*~", "*.pyo", "*#", ".#*", "*.lock", "*.log*", "*.orig"],
            dirs = [__cwd__]
            ),
        ),
    )

__all__ = ['clean']


@task
def clean(options, info):
    """Clean up.

    options.paved.clean_dirs: directories to search recursively
    options.paved.clean_patterns: patterns to search for and remove
    """
    info("Cleaning patterns %s", options.paved.clean.patterns)
    for wd in options.paved.clean.dirs:
        info("Cleaning in %s", wd)
        for p in options.paved.clean.patterns:
            for f in wd.walkfiles(p):
                f.remove()
