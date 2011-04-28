# -*- coding: utf-8 -*-
"""paved -- common paver tasks.
"""
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

    options.paved.dirs: directories to search recursively
    options.paved.patterns: patterns to search for and remove
    """
    info("Cleaning patterns %s", options.paved.clean.patterns)
    for wd in options.paved.clean.dirs:
        info("Cleaning in %s", wd)
        for p in options.paved.clean.patterns:
            for f in wd.walkfiles(p):
                f.remove()

@task
def printoptions():
    '''print paver options.
    
    Prettified by json.
    `long_description` is removed
    '''
    def replace_set(obj):
        if isinstance(obj, dict):
            for k,v in obj.items():
                if isinstance(v, set):
                    obj[k]=list(v)
                replace_set(v)
                if k=='long_description':
                    obj[k]='[not displayed]'
                
        return obj
    x = replace_set(environment.options)
    orig = json.dumps(x, indent=4)
    print orig
