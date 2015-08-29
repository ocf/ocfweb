import os
from collections import namedtuple
from itertools import chain
from os.path import dirname
from os.path import isfile
from os.path import join
from os.path import realpath
from os.path import relpath
from os.path import splitext

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from ocfweb.markdown import markdown_and_meta

DOCS_DIR = join(dirname(__file__), 'docs')


class Document(namedtuple('Document', ['name', 'meta', 'html'])):

    @classmethod
    def from_name(cls, name):
        """Return an instantiated document object.

        Checks the document name for illegal characters and attempts at path
        traversal; it's OK to call this method with untrusted input.
        """
        # the url mapping should do this already; this is just a sanity check in
        # case anybody changes it in the future without thinking
        assert '.' not in name, 'name shouldn\'t have dot: {}'.format(name)
        assert name.startswith('/'), 'name should start with slash: {}'.format(name)

        # We want to do something like:
        #     join(dirname(__file__), 'docs', name + '.md')
        # ...but we need to be careful to avoid path traversal when using
        # os.path.join (e.g. if the name contains '//')
        path = DOCS_DIR
        for component in name[1:].split('/'):
            if len(component) == 0:
                raise ValueError('Illegal document name.')
            path = join(path, component)
        path = realpath(path + '.md')

        if not isfile(path):
            raise ValueError('Document does not exist.')

        # sanity check that the file is under the directory we expect
        assert path.startswith(realpath(DOCS_DIR) + '/')

        with open(path) as f:
            html, meta = markdown_and_meta(f.read())

        if 'title' not in meta:
            raise ValueError('Document lacks required title meta variable.')

        return cls(
            name=name,
            meta=meta,
            html=html,
        )

    @property
    def category(self):
        return self.name.rsplit('/', 1)[0] + '/'


def list_doc_names():
    """Return a list of document names.

    Only *documents* are included in the list. In particular, there's no
    guarantee that a category without a document at its root will appear in the
    list. (Categories with documents at the root will, though.)

    >>> list_doc_names()
    ['services/shell', 'services/webapps', 'services']
    """
    start = join(dirname(__file__), 'docs')
    return [
        '/' + splitext(relpath(path, start))[0]
        for path in
        chain.from_iterable(
            [join(dirpath, f) for f in filenames]
            for dirpath, dirnames, filenames
            in os.walk(start)
        )
        if path.endswith('.md')
    ]


def list_docs():
    """Returns a dict of document objects.

    The full document content plus metadata is retrieved, so this is pretty
    slow (but is cached, so usually plenty fast).
    """
    return {
        doc_name: Document.from_name(doc_name)
        for doc_name in list_doc_names()
    }


def docs_index(request):
    return render_to_response(
        'index.html',
        {
            'title': 'Documentation',
        },
        context_instance=RequestContext(request),
    )


def doc(request, doc_name):
    doc_name = '/' + doc_name
    try:
        doc = Document.from_name(doc_name)
    except ValueError:
        raise Http404()

    return render_to_response(
        doc.meta.get('template', 'doc.html'),
        {
            'title': doc.meta['title'],
            'doc': doc,
        },
        context_instance=RequestContext(request),
    )
