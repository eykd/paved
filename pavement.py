# -*- coding: utf-8 -*-
"""pavement.py -- pavement for paved.

Copyright 2010 David Eyk. All rights reserved.
"""
import site

import warnings
warnings.filterwarnings('ignore', "Parent module 'pavement' not found while handling absolute import")

from paver.easy import *
from paver.setuputils import setup

__path__ = path(__file__).abspath().dirname()
site.addsitedir(__path__)

from paved import *
from paved.dist import *

__path__ = path(__file__).abspath().dirname()
site.addsitedir(__path__)


setup(
    name = "Paved",
    version = "0.1",
    packages=['paved'],
    url = "https://github.com/eykd/paved",
    download_url = "http://pypi.python.org/pypi/Paved/",
    author = "David Eyk",
    author_email = "eykd@eykd.net",
    license = 'BSD',

    description = 'Common tasks for Paver-based projects.',
    long_description = open('README.rst').read(),

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
