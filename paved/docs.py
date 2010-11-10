# -*- coding: utf-8 -*-
"""paved.sphinx -- helpers and tasks for Sphinx documentation.
"""
from paver.easy import task, sh, path, options, Bunch
from paver.tasks import Task
from sphinx.ext import autodoc

from . import paved
from . import util

util.update(
    options.paved,
    dict(
        docs = Bunch(
            path = path('./docs'),
            targets = ['html']
            ),
        )
    )

__all__ = ['TaskDocumenter', 'documentTasks', 'sphinx_make', 'docs', 'clean_docs']


class TaskDocumenter(autodoc.FunctionDocumenter):
    """Allow autodoc to document paver tasks.

    Lifted straight out of Paver's sphinx conf.py:

    http://code.google.com/p/paver/source/browse/trunk/docs/source/conf.py
    """
    objtype = "task"
    directivetype = "function"
    
    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, Task)
        
    def import_object(self):
        super(TaskDocumenter, self).import_object()
        obj = self.object
        self.object = obj.func
        return True


def documentTasks():
    """Add documentation for tasks. Call this from your sphinx conf.py
    """
    autodoc.add_documenter(TaskDocumenter)


def sphinx_make(*targets):
    """Call the Sphinx Makefile with the specified targets.
    """
    sh('make %s' % ' '.join(targets), cwd=options.paved.docs.path)


@task
def docs():
    """Make Sphinx docs.
    """
    sphinx_make(*options.paved.docs.targets)


@task
def clean_docs():
    """Clean Sphinx docs.
    """
    sphinx_make('clean')