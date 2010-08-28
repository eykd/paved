# -*- coding: utf-8 -*-
"""paved.pkg -- packaging tools for paved.

Automatically 

Copyright 2010 David Eyk. All rights reserved.
"""
from paver.easy import sh, task, consume_args

from . import paved


__all__ = ['pip_install', 'easy_install']


@task
@consume_args
def pip_install(args):
    sh('pip install %s' % (' '.join(args)))


@task
@consume_args
def easy_install(args):
    sh('easy_install %s' % (' '.join(args)))
