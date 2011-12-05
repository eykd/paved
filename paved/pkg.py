# -*- coding: utf-8 -*-
"""paved.pkg -- packaging tools for paved.
"""
from paver.easy import sh, task, consume_args, options, Bunch

from . import paved
from . import util


__all__ = ['pip_install', 'easy_install']


@task
@consume_args
def pip_install(args):
    """Send the given arguments to `pip install`.
    """
    util.pip_install(*args)


@task
def easy_install(args):
    """Send the given arguments to `easy_install`.
    """
    util.easy_install(*args)
