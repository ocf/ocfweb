import os
from itertools import chain
from os.path import dirname
from os.path import isfile
from os.path import join
from os.path import relpath
from os.path import splitext

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from ocfweb.markdown import markdown_and_meta


def docs_index(request):
    start = join(dirname(__file__), 'docs')
    links = [
        splitext(relpath(path, start))[0]
        for path in
        chain.from_iterable(
            [join(dirpath, f) for f in filenames]
            for dirpath, dirnames, filenames
            in os.walk(start)
        )
        if path.endswith('.md')
    ]

    return render_to_response(
        'index.html',
        {
            'title': 'Documentation',
            'links': links,
        },
        context_instance=RequestContext(request),
    )


def doc(request, doc_name):
    # the url mapping should do this already; this is just a sanity check in
    # case anybody changes it in the future without thinking
    assert '.' not in doc_name

    # safer way to do join(dirname(__file__), 'docs', doc_name + '.md')
    path = join(dirname(__file__), 'docs')
    for component in doc_name.split('/'):
        if len(component) == 0:
            print('fail upper')
            raise Http404()
        path = join(path, component)
    path += '.md'

    if not isfile(path):
        print('fail lower')
        raise Http404()

    with open(path) as f:
        content, meta = markdown_and_meta(f.read())

    if 'title' not in meta:
        raise ValueError('Document lacks required title meta variable.')

    return render_to_response(
        'doc.html',
        {
            'title': meta['title'],
            'content': content,
        },
        context_instance=RequestContext(request),
    )
