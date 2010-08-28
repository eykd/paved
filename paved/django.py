# -*- coding: utf-8 -*-
"""paved.django -- common tasks for django projects.

Copyright 2010 David Eyk. All rights reserved.
"""
from paver.easy import options, sh, task, consume_args, Bunch

from . import paved

options.paved.update(
    django = Bunch(
        manage_py = None,
        ),
    )

__all__ = ['manage', 'call_manage']


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
