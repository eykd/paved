# -*- coding: utf-8 -*-
"""paved.django -- common tasks for django projects.

Copyright 2010 David Eyk. All rights reserved.
"""
from paver.easy import options, task, consume_args, error, path, Bunch
from paver.runtime import BuildFailure

from . import paved
from . import util

options.paved.update(
    django = Bunch(
        manage_py = None,
        project = None,
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


def call_manage(cmd):
    project = options.paved.django.project
    if project is None:
        raise BuildFailure("No project path defined. Use: options.paved.django.project = 'path.to.project'")
    manage_py = options.paved.django.manage_py
    if manage_py is None:
        manage_py = 'django-admin.py'
    else:
        manage_py = 'cd {manage_py.parent}; python ./{manage_py.name}'.format(**locals())
    util.shv('{manage_py} {cmd} --settings={project}'.format(**locals()))


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
def shell(info):
    """Run the ipython shell.
    """
    try:
        import django_extensions
        call_manage('shell_plus')
    except ImportError:
        info("Could not import django_extensions. Using default shell. ")
        call_manage('shell')


@task
def start():
    """Run the dev server.
    """
    try:
        call_manage('runserver_plus')
    except BuildFailure:
        call_manage('runserver')
