import re
from collections import namedtuple
from operator import attrgetter

from django import template
from django.utils.html import strip_tags

from ocfweb.docs.urls import DOCS


class Node(namedtuple('Node', ['path', 'title', 'children'])):

    @property
    def url_path(self):
        return self.path.lstrip('/').rstrip('/')


register = template.Library()


@register.inclusion_tag('docs/partials/doc-tree.html')
def doc_tree(root='/', suppress_root=True, cur_path=None, exclude='$^'):
    # root is expected to be like '/' or '/services/' or '/services/web/'
    assert root.startswith('/')
    assert root.endswith('/')

    exclude = re.compile(exclude)

    def _make_tree(root):
        path = root[:-1]
        doc = DOCS.get(path)
        return Node(
            path=path,
            title=doc.title if doc else root,
            children=sorted(
                [
                    _make_tree(child)
                    for child in
                    {
                        root + doc.name[len(root):].split('/', 1)[0] + '/'
                        for doc in DOCS.values()
                        if doc.name.startswith(root) and not exclude.match(doc.name)
                    }
                ],
                key=attrgetter('path'),
            ),
        )

    return {
        'tree': _make_tree(root),
        'suppress_root': suppress_root or root == '/',
        'cur_path': cur_path,
    }


@register.inclusion_tag('docs/partials/doc-toc.html')
def doc_toc(toc, collapsible=False):
    if len(toc) > 3:  # heuristic to avoid dumb tables of contents
        levels = list(sorted({entry[0] for entry in toc}))
        cur = levels[0]

        html = '<ol>'

        for level, text, id in toc:
            while cur > level:
                html += '</ol>'
                cur -= 1
            while cur < level:
                html += '<ol>'
                cur += 1
            html += '<li><a href="#{fragment}">{text}</a></li>'.format(
                fragment=id,
                text=strip_tags(text),
            )

        while cur > levels[0]:
            html += '</ol>'
            cur -= 1

        html += '</ol>'
    else:
        html = ''

    return {
        'html': html,
        'collapsible': collapsible,
    }


@register.inclusion_tag('docs/partials/doc-categories.html')
def doc_categories(root, categories):
    return {
        'categories': [
            (
                category_name,
                [
                    (root[1:] + child, DOCS.get(root + child).title)
                    for child in children
                ],
            )
            for category_name, children in categories
        ],
    }
