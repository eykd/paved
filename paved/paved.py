# -*- coding: utf-8 -*-
"""paved -- common paver tasks.
"""
from json.encoder import JSONEncoder
from paver.easy import options, path, task, Bunch, environment, needs
import json

__cwd__ = path('.').abspath()


options(
    paved = Bunch(
        cwd = __cwd__,
        
        clean = Bunch(
            patterns = ["*.pyc", "*~", "*.pyo", "*#", ".#*", "*.lock", "*.log*", "*.orig"],
            dirs = [__cwd__]
            ),
        ),
    )

__all__ = ['clean', 'printoptions']


@task
@needs('paver.doctools.doc_clean')
def clean(options, info):
    """Clean up extra files littering the source tree.

    options.paved.clean.dirs: directories to search recursively
    options.paved.clean.patterns: patterns to search for and remove
    """
    info("Cleaning patterns %s", options.paved.clean.patterns)
    for wd in options.paved.clean.dirs:
        info("Cleaning in %s", wd)
        for p in options.paved.clean.patterns:
            for f in wd.walkfiles(p):
                f.remove()

class MyEncoder (JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        
        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return str(o)

@task
def printoptions():
    '''print paver options.
    
    Prettified by json.
    `long_description` is removed
    '''
    x = json.dumps(environment.options,
                   indent=4,
                   sort_keys=True,
                   skipkeys=True,
                   cls=MyEncoder)
    print x
