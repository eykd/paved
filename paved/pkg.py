# -*- coding: utf-8 -*-
"""paved.pkg -- packaging tools for paved.

Copyright 2010 David Eyk. All rights reserved.
"""
import urllib

from paver.easy import sh, task, consume_args, options, Bunch

from . import paved

options.paved.update(
    pkg = Bunch(
        distribute_url = 'http://python-distribute.org/distribute_setup.py',
        )
    )

__all__ = ['get_distribute', 'pip_install', 'easy_install']


@task
def get_distribute(options):
    """Retrieve a copy of distribute_setup.py for distribution.
    """
    url = urllib.urlopen(options.paved.pkg.distribute_url)
    with open(options.paved.cwd / 'distribute_setup.py', 'w') as fo:
        fo.write(url.read())


@task
@consume_args
def pip_install(args):
    sh('pip install %s' % (' '.join(args)))


@task
@consume_args
def easy_install(args):
    sh('easy_install %s' % (' '.join(args)))
