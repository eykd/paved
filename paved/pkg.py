# -*- coding: utf-8 -*-
"""paved.pkg -- packaging tools for paved.
"""
from paver.easy import sh, task, consume_args

from . import paved

__all__ = ['pip_install', 'easy_install']


@task
@consume_args
def pip_install(*args):
    """Send the given arguments to `pip install`.
    """
    sh('pip install %s' % (' '.join(args)))


@task
@consume_args
def easy_install(*args):
    """Send the given arguments to `easy_install`.
    """
    sh('easy_install %s' % (' '.join(args)))
