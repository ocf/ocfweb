"""Documents backed by Markdown.

This is the most common type of doc. It reads a Markdown file and renders it in
a standard template.

Markdown documents can specify the meta attributes:

    - [[!meta title="Page title"]]
      Changes the page title; all templates must specify this.

    - [[!meta template="my_template.html"]]
      Changes the page template; most templates should *not* specify this,
      unless they want to customize something (e.g. the sidebar)
"""
import os
from functools import partial
from pathlib import Path

from django.conf import settings
from django.shortcuts import render

from ocfweb.component.markdown import markdown_and_toc
from ocfweb.component.markdown import text_and_meta
from ocfweb.docs.doc import Document


DOCS_DIR = Path(__file__).parent.joinpath('docs')


def render_markdown_doc(meta, text, doc, request):

    # Reload markdown docs if in development
    if settings.DEBUG:
        with doc.path.open() as f:
            text, meta = text_and_meta(f)

    html, toc = markdown_and_toc(text)

    return render(
        request,
        meta.get('template', 'doc.html'),
        {
            'title': meta['title'],
            'doc': doc,
            'html': html,
            'toc': toc,
        },
    )


def get_markdown_docs():
    for path in DOCS_DIR.glob('**/*.md'):
        name, _ = os.path.splitext(str(path.relative_to(DOCS_DIR)))

        # sanity check that the file is under the directory we expect
        assert DOCS_DIR in path.parents

        with path.open() as f:
            text, meta = text_and_meta(f)

        if 'title' not in meta:
            raise ValueError('Document {} lacks required title meta variable.'.format(name))

        yield Document(
            name='/' + name,
            title=meta['title'],
            render=partial(render_markdown_doc, meta, text),
            path=path,
        )
