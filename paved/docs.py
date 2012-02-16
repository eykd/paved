# -*- coding: utf-8 -*-
"""paved.sphinx -- helpers and tasks for Sphinx documentation.
"""
from . import paved, util
from paver.easy import task, needs, sh, path, options, Bunch, BuildFailure


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

__all__ = ['sphinx_make', 'docs', 'clean_docs', 'rsync_docs', 'ghpages', 'showhtml']


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

@task
def ghpages():
    '''Push Sphinx docs to github_ gh-pages branch.
    
     1. Create file .nojekyll
     2. Push the branch to origin/gh-pages 
        after committing using ghp-import_
    
    Requirements:
     - easy_install ghp-import

    Options:
     - `options.paved.docs.*` is not used
     - `options.sphinx.docroot` is used (default=docs)
     - `options.sphinx.builddir` is used (default=.build)
     
    .. warning::
        This will DESTROY your gh-pages branch. 
        If you love it, you'll want to take backups 
        before playing with this. This script assumes 
        that gh-pages is 100% derivative. You should 
        never edit files in your gh-pages branch by hand 
        if you're using this script because you will 
        lose your work.
     
    .. _github: https://github.com 
    .. _ghp-import: https://github.com/davisp/ghp-import 
    '''
    
    # copy from paver
    opts = options
    docroot = path(opts.get('docroot', 'docs'))
    if not docroot.exists():
        raise BuildFailure("Sphinx documentation root (%s) does not exist."
                           % docroot)
    builddir = docroot / opts.get("builddir", ".build")
    # end of copy
    
    builddir=builddir / 'html'
    if not builddir.exists():
        raise BuildFailure("Sphinx build directory (%s) does not exist."
                           % builddir)
    
    nojekyll = path(builddir) / '.nojekyll'
    nojekyll.touch()
    
    sh('ghp-import -p %s' % (builddir))
    


@task
def showhtml():
    """Open your web browser and display the generated html documentation.
    """
    import webbrowser

    # copy from paver
    opts = options
    docroot = path(opts.get('docroot', 'docs'))
    if not docroot.exists():
        raise BuildFailure("Sphinx documentation root (%s) does not exist."
                           % docroot)
    builddir = docroot / opts.get("builddir", ".build")
    # end of copy
    
    builddir=builddir / 'html'
    if not builddir.exists():
        raise BuildFailure("Sphinx build directory (%s) does not exist."
                           % builddir)

    webbrowser.open(builddir / 'index.html')
        