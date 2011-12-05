# -*- coding: utf-8 -*-
"""paved.pkg -- packaging tools for paved.
"""
from paver.easy import sh, task, consume_args, options, Bunch

from . import paved
from . import util


__all__ = ['pip_install', 'easy_install']


util.update(
    options.paved,
    dict(
        pip = Bunch(
            download_cache = '',
            ),
        )
    )



def pip_install(*args):
    """Send the given arguments to `pip install`.
    """
    download_cache = ('--download_cache=%s ' % options.paved.pip.download_cache) if options.paved.pip.download_cache else ''
    sh('pip install %s%s' % (download_cache, ' '.join(args)))


def easy_install(*args):
    """Send the given arguments to `easy_install`.
    """
    sh('easy_install %s' % (' '.join(args)))
