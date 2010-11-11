# -*- coding: utf-8 -*-
"""paved.sphinx -- helpers and tasks for Sphinx documentation.
"""
from paver.easy import task, sh, path, options, Bunch

from . import paved
from . import util

util.update(
    options.paved,
    dict(
        docs = Bunch(
            path = path('./docs'),
            targets = ['html']
            ),
        )
    )

__all__ = ['sphinx_make', 'docs', 'clean_docs']


def sphinx_make(*targets):
    """Call the Sphinx Makefile with the specified targets.
    """
    sh('make %s' % ' '.join(targets), cwd=options.paved.docs.path)


@task
def docs():
    """Make Sphinx docs.
    """
    sphinx_make(*options.paved.docs.targets)


@task
def clean_docs():
    """Clean Sphinx docs.
    """
    sphinx_make('clean')
