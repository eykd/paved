# -*- coding: utf-8 -*-
"""pycheck -- check python code.
"""
from . import util
from paver.easy import options, task, sh, needs, path
from paver.options import Bunch


__all__ = ['pycheckall', 'sloccount', 'findimports', 'pyflakes', 'pychecker', 'nose']


util.update(
    options.paved,
    dict(
        pycheck=Bunch(
            nose=Bunch(
                         param='--with-xunit --verbose',
                         ),
            sloccount=Bunch(
                         param='--wide --details',
                         ),
            findimports=Bunch(
                         param='',
                         ),
            pyflakes=Bunch(
                         param='',
                         ),
            pychecker=Bunch(
                         param='--stdlib --only --limit 100',
                         ),
            ),
        )
    )

@task
def sloccount():
    '''Print "Source Lines of Code" and export to file.
    
    Export is hudson_ plugin_ compatible: sloccount.sc
    
    requirements:
     - sloccount_ should be installed.
     - tee and pipes are used

    options.paved.pycheck.sloccount.param

    .. _sloccount: http://www.dwheeler.com/sloccount/
    .. _hudson: http://hudson-ci.org/
    .. _plugin: http://wiki.hudson-ci.org/display/HUDSON/SLOCCount+Plugin
    '''

    # filter out  subpackages
    setup = options.get('setup')
    packages = options.get('packages') if setup else None
        
    if packages:
        dirs = [x for x in packages if '.' not in x]
    else:
        dirs = ['.']
    
    # sloccount has strange behaviour with directories, 
    # can cause exception in hudson sloccount plugin.
    # Better to call it with file list
    ls=[]
    for d in dirs:
        ls += list(path(d).walkfiles())
    #ls=list(set(ls))
    files=' '.join(ls)
    param=options.paved.pycheck.sloccount.param
    sh('sloccount {param} {files} | tee sloccount.sc'.format(param=param, files=files))

@task
def findimports():
    '''print python module dependencies by findimports.
       
    requirements:
     - findimports_ should be installed. ``easy_install findimports``

    options.paved.pycheck.findimports.param

    .. _findimports: http://pypi.python.org/pypi/findimports
    '''

    # filter out  subpackages
    packages = [x for x in options.setup.packages if '.' not in x]

    sh('findimports {param} {files} '.format(param=options.paved.pycheck.findimports.param, files=' '.join(packages)))

@task
def pyflakes():
    '''passive check of python programs by pyflakes.
       
    requirements:
     - pyflakes_ should be installed. ``easy_install pyflakes``

    options.paved.pycheck.pyflakes.param

    .. _pyflakes: http://pypi.python.org/pypi/pyflakes
    '''

    # filter out  subpackages
    packages = [x for x in options.setup.packages if '.' not in x]

    sh('pyflakes {param} {files}'.format(param=options.paved.pycheck.pyflakes.param, files=' '.join(packages)))

@task
def pychecker():
    '''check of python programs by pychecker.
       
    requirements:
     - pychecker_ should be installed.

    options.paved.pycheck.pychecker.param

    .. _pychecker: http://pychecker.sourceforge.net/
    '''

    # filter out  subpackages
    packages = [x for x in options.setup.packages if '.' not in x]

    sh('pychecker  {param} {files}'.format(param=options.paved.pycheck.pychecker.param, files=' '.join(packages)))

@task
def nose():
    '''Run unit tests using nosetests.
       
    requirements:
     - nose_ should be installed.

    options.paved.pycheck.nose.param
    
    .. _nose: http://somethingaboutorange.com/mrl/projects/nose/1.0.0/
    '''
    sh('nosetests {param}'.format(param=options.paved.pycheck.nose.param))

@task
@needs('sloccount', 'pychecker', 'pyflakes', 'findimports', 'nose')
def pycheckall():
    '''All pycheck tasks.
    '''
