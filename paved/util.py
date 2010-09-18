# -*- coding: utf-8 -*-
"""paved.util -- helper functions.

Copyright 2010 David Eyk. All rights reserved.
"""
import re
from paver.easy import info, options, path, dry, sh, error

from . import paved

try:
    if not options.virtualenv.activate_cmd:
        raise AttributeError
except AttributeError:
    options.setdotted('virtualenv.activate_cmd', 'source ' + options.paved.cwd / 'source' / 'bin' / 'activate')


__all__ = ['rmFilePatterns', 'rmDirPatterns', 'shv']


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


def shv(command, capture=False, ignore_error=False, cwd=None):
    """Run the given command inside the virtual environment, if available:
    """
    try:
        command = "%s; %s" % (options.virtualenv.activate_cmd, command)
    except AttributeError:
        pass
    return sh(command, capture=capture, ignore_error=ignore_error, cwd=cwd)
