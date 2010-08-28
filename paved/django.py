# -*- coding: utf-8 -*-
"""paved.django -- common tasks for django projects.

Copyright 2010 David Eyk. All rights reserved.
"""
from paver.easy import options, sh, task, consume_args, Bunch
from paver.runtime import BuildFailure

from . import paved

options.paved.update(
    django = Bunch(
        manage_py = None,
        syncdb = Bunch(
            fixtures = [],
            ),
        ),
    )

__all__ = ['manage', 'call_manage', 'test', 'syncdb', 'shell', 'start']


@task
@consume_args
def manage(args):
    """Run the provided commands against Django's manage.py
    """
    args = ' '.join(args)
    call_manage(args)


def call_manage(cmd, error):
    manage_py = options.paved.django.manage_py
    if manage_py is None:
        error("No manage.py defined. Use: options.paved.django(manage_py = 'path_to_manage_py')")
        raise ValueError()
    sh('python {manage_py} {cmd}'.format(**locals()))


@task
@consume_args
def test(args):
    """Run tests.
    """
    cmd = args and 'test %s' % ' '.join(options.args) or 'test'
    call_manage(cmd)


@task
@consume_args
def syncdb(args):
    """Update the database with model schema.
    """
    cmd = args and 'syncdb %s' % ' '.join(options.args) or 'syncdb --noinput'
    call_manage(cmd)
    for fixture in options.paved.django.syncdb.fixtures:
        call_manage("loaddata %s" % fixture)


@task
def shell():
    """Run the ipython shell.
    """
    try:
        call_manage('shell_plus')
    except BuildFailure:
        call_manage('shell')


@task
def start():
    """Run the dev server.
    """
    try:
        call_manage('runserver_plus')
    except BuildFailure:
        call_manage('runserver')
