# -*- coding: utf-8 -*-
"""paved.dist -- distribution tasks

Copyright 2010 David Eyk. All rights reserved.
"""
import urllib

from paver.easy import task, needs, options, Bunch
from paver.setuputils import install_distutils_tasks

from . import paved

install_distutils_tasks()

options.paved.update(
    dist = Bunch(
        distribute_url = 'http://python-distribute.org/distribute_setup.py',
        )
    )

__all__ = ['get_distribute', 'sdist']


@task
def get_distribute(options):
    """Retrieve a copy of distribute_setup.py for distribution.
    """
    url = urllib.urlopen(options.paved.dist.distribute_url)
    with open(options.paved.cwd / 'distribute_setup.py', 'w') as fo:
        fo.write(url.read())


@task
@needs('get_distribute', 'generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass


@task
@needs('sdist', 'setuptools.command.upload')
def upload():
    """Overrides upload to make sure sdist is run.
    """
    pass
