import re
from collections import namedtuple

import dateutil.parser
from bs4 import BeautifulSoup
from cached_property import cached_property
from django.utils.html import strip_tags
from django.utils.html import urlize
from lxml import etree

from ocfweb.caching import ttl_cache


_namespaces = {'atom': 'http://www.w3.org/2005/Atom'}


class Post(namedtuple('Post', [
    'id',
    'published',
    'updated',
    'title',
    'content',
    'author_name',
    'author_email',
    'link',
])):

    @cached_property
    def content_snippet(self):
        return ''.join(
            '<p>' + paragraph + '</p>'
            for paragraph in
            filter(
                None,
                (
                    urlize(BeautifulSoup(strip_tags(piece), 'lxml').get_text().strip())
                    for piece in re.split(r'\n|(?:<br\s*/?\s*>?)', self.content)
                ),
            )
        )

    @classmethod
    def from_element(cls, element):
        def grab_attr(attr):
            el = element
            for part in attr.split('_'):
                el = el.find('atom:' + part, namespaces=_namespaces)
            return el.text

        attrs = {
            attr: grab_attr(attr)
            for attr in cls._fields
        }
        attrs['updated'] = dateutil.parser.parse(attrs['updated'])
        attrs['published'] = dateutil.parser.parse(attrs['published'])
        attrs['link'] = element.xpath(
            'atom:link[@type="text/html"]',
            namespaces=_namespaces,
        )[0].get('href')
        return cls(**attrs)


@ttl_cache(ttl=60)
def get_blog_posts():
    """Parse the beautiful OCF status blog atom feed into a list of Posts."""
    tree = etree.parse('http://status.ocf.berkeley.edu/feeds/posts/default')
    return [
        Post.from_element(post)
        for post in tree.xpath(
            '//atom:entry',
            namespaces=_namespaces,
        )
    ]
