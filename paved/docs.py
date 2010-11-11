# -*- coding: utf-8 -*-
"""paved.sphinx -- helpers and tasks for Sphinx documentation.
"""
from paver.easy import task, needs, sh, path, options, Bunch

from . import paved
from . import util

util.update(
    options.paved,
    dict(
        docs = Bunch(
            path = path('./docs'),
            targets = ['html'],
            build_rel = '_build/html',
            upload_location = False,
            ),
        )
    )

__all__ = ['sphinx_make', 'docs', 'clean_docs', 'rsync_docs']


def sphinx_make(*targets):
    """Call the Sphinx Makefile with the specified targets.

    `options.paved.docs.path`: the path to the Sphinx folder (where the Makefile resides).
    """
    sh('make %s' % ' '.join(targets), cwd=options.paved.docs.path)


@task
def docs():
    """Make Sphinx docs.

    `options.paved.docs.path`: the path to the Sphinx folder (where the Makefile resides).

    `options.paved.docs.targets`: the Make targets to send to `sphinx_make`. Default is `html`.
    """
    sphinx_make(*options.paved.docs.targets)


@task
def clean_docs():
    """Clean Sphinx docs.

    `options.paved.docs.path`: the path to the Sphinx folder (where the Makefile resides).
    """
    sphinx_make('clean')


@task
@needs('docs')
def rsync_docs():
    """Upload the docs to a remote location via rsync.

    `options.paved.docs.rsync_location`: the target location to rsync files to.
    
    `options.paved.docs.path`: the path to the Sphinx folder (where the Makefile resides).

    `options.paved.docs.build_rel`: the path of the documentation
        build folder, relative to `options.paved.docs.path`.
    """
    assert options.paved.docs.rsync_location, "Please specify an rsync location in options.paved.docs.rsync_location."
    sh('rsync -ravz %s/ %s/' % (path(options.paved.docs.path) / options.paved.docs.build_rel, 
                                options.paved.docs.rsync_location))
