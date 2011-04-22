# -*- coding: utf-8 -*-
"""paved.dist -- distribution tasks
"""
import urllib

from paver.easy import task, needs, options, path, Bunch
from paver.setuputils import install_distutils_tasks

from . import paved
from . import util

install_distutils_tasks()

util.update(
    options.paved, 
    dict(
        dist = Bunch(
            distribute_url = 'http://python-distribute.org/distribute_setup.py',
            manifest = Bunch(
                include = set([
                        "distribute_setup.py",
                        "pavement.py",
                        "paver-minilib.zip",
                        "setup.py",
                        "CHANGES*",
                        "LICENSE*",
                        "README*",
                        "TODO*",
                        ]),
                recursive_include = set([]),
                prune = set([]),
                include_sphinx_docroot=True,
                exclude_sphinx_builddir=True,                
                ),
            )
        )
    )

__all__ = ['get_distribute', 'sdist', 'upload', 'manifest']


@task
def get_distribute(options):
    """Retrieve a copy of distribute_setup.py for distribution.

    `options.paved.dist.distribute_url`: the URL to download the
    `distribute_setup.py` file from.
    """
    url = urllib.urlopen(options.paved.dist.distribute_url)
    with open(options.paved.cwd / 'distribute_setup.py', 'w') as fo:
        fo.write(url.read())


@task
def manifest():
    """Guarantee the existence of a basic MANIFEST.in.

    manifest doc: http://docs.python.org/distutils/sourcedist.html#manifest
    
    `options.paved.dist.manifest.include`: set of files (or globs) to include with the `include` directive.

    `options.paved.dist.manifest.recursive_include`: set of files (or globs) to include with the `recursive-include` directive.

    `options.paved.dist.manifest.prune`: set of files (or globs) to exclude with the `prune` directive.
    
    `options.paved.dist.manifest.include_sphinx_docroot`: True -> sphinx docroot is added as `grant`
    
    `options.paved.dist.manifest.include_sphinx_docroot`: True -> sphinx builddir is added as `prune`
    """
    prune = options.paved.dist.manifest.prune
    grant = set()
    
    
    if options.paved.dist.manifest.include_sphinx_docroot:
        docroot = options.get('docroot', 'docs')
        grant.update([docroot])
    
        if options.paved.dist.manifest.exclude_sphinx_builddir:
            builddir = docroot + '/' + options.get("builddir", ".build")
            prune.update([builddir])
         
    with open(options.paved.cwd / 'MANIFEST.in', 'w') as fo:
        for item in grant:
            fo.write('grant %s\n' % item)
        for item in options.paved.dist.manifest.include:
            fo.write('include %s\n' % item)
        for item in options.paved.dist.manifest.recursive_include:
            fo.write('recursive-include %s\n' % item)
        for item in prune:
            fo.write('prune %s\n' % item)


@task
@needs('get_distribute', 'generate_setup', 'minilib', 'manifest', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated.
    """
    pass


@task
@needs('sdist', 'setuptools.command.upload')
def upload():
    """Upload the package to PyPI.
    """
    pass
