from collections import namedtuple
from typing import Any
from typing import Dict
from typing import List
from xml.etree import ElementTree as etree

import dateutil.parser
import requests
from cached_property import cached_property
from requests.exceptions import RequestException

from ocfweb.caching import periodic

_namespaces = {'atom': 'http://www.w3.org/2005/Atom'}


class Post(
    namedtuple(
        'Post', [
            'id',
            'published',
            'updated',
            'title',
            'content',
            'author_name',
            'author_email',
            'link',
        ],
    ),
):

    @cached_property
    def datetime(self) -> bool:
        return self.published

    @classmethod
    def from_element(cls: Any, element: Any) -> Any:
        def grab_attr(attr: str) -> str:
            el: Any = element
            for part in attr.split('_'):
                el = el.find('atom:' + part, namespaces=_namespaces)
            return el.text

        attrs: Dict[str, Any] = {
            attr: grab_attr(attr)
            for attr in cls._fields
        }
        attrs['updated'] = dateutil.parser.parse(attrs['updated'])
        attrs['published'] = dateutil.parser.parse(attrs['published'])
        # Fix builtin function being typed as returning an int on error, which has no get
        el_find: Any = element.find(
            './/atom:link[@type="text/html"]',
            namespaces=_namespaces,
        )
        attrs['link'] = el_find.get('href')
        return cls(**attrs)


@periodic(60)
def get_blog_posts() -> List[Any]:
    """Parse the beautiful OCF status blog atom feed into a list of Posts.

    Unfortunately Blogger is hella flakey so we use it inside a loop and fail
    silently if it doesn't succeed.
    """
    for _ in range(5):
        try:
            tree = etree.fromstring(
                requests.get(
                    'https://status.ocf.berkeley.edu/feeds/posts/default',
                    timeout=2,
                ).content,
            )
        except RequestException:
            pass
        else:
            break
    else:
        # fail silently
        return []

    return [
        Post.from_element(post)
        for post in tree.findall(
            './/atom:entry',
            namespaces=_namespaces,
        )
    ]
