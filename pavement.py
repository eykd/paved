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

__path__ = path(__file__).abspath().dirname()
site.addsitedir(__path__)


setup(
    name="Paved",
    version="0.1",
    url="http://eykd.net/",
    author="David Eyk",
    author_email="eykd@eykd.net",

    py_modules=['paved'],
    )
