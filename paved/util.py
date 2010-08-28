# -*- coding: utf-8 -*-
"""paved.util -- helper functions.

Copyright 2010 David Eyk. All rights reserved.
"""
import re
from paver.easy import info, options, path, dry


def _walkWithAction(*patterns, **kwargs):
    use_path = path(kwargs.get('use_path', options.paved.cwd))
    action = kwargs.pop('action')
    assert type(action) is str
    assert hasattr(use_path, action)

    use_regex = kwargs.get('use_regex')
    errors = kwargs.get('errors', 'warn')
    walk_method = kwargs.get('walk_method', 'walkfiles')

    for p in patterns:
        info("Looking for %s" % p)
        if use_regex:
            cp = re.compile(p)
            p = None
        for f in getattr(use_path, walk_method)(pattern=p, errors=errors):
            if use_regex and not cp.search(str(f)):
                continue
            if f.exists():
                msg = "%s %s..." % (action, f)
                dry(msg, getattr(f, action))
    

def rmFilePatterns(*patterns, **kwargs):
    """Remove all files under the given path with the given patterns.
    """
    kwargs['action'] = 'remove'
    kwargs['walk_method'] = 'walkfiles'
    return _walkWithAction(*patterns, **kwargs)


def rmDirPatterns(*patterns, **kwargs):
    """Remove all directories under the current path with the given patterns.
    """
    kwargs['action'] = 'rmtree'
    kwargs['walk_method'] = 'walkdirs'
    return _walkWithAction(*patterns, **kwargs)
