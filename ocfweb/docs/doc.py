from collections import namedtuple

from cached_property import cached_property
from django.db import models


class DocText(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __init__(self, title, text):
        self.title = title
        self.text = text


class Document(namedtuple('Document', ['name', 'title', 'render'])):

    @cached_property
    def category(self):
        """Return full category path of the document.

        For example, "/" or "/staff/backend/".
        """
        return self.name.rsplit('/', 1)[0] + '/'

    @cached_property
    def category_for_sidebar(self):
        """Return the category to show similar pages for in the sidebar.

        If this page isn't at the root category, we just return this page's
        category.

        If this page is at the root category, we return the category rooted at
        this page (which may or may not have any pages in it).
        """
        if self.category == '/':
            return self.name + '/'
        else:
            return self.category

    @cached_property
    def edit_url(self):
        """Return a GitHub edit URL for this page."""
        return (
            'https://github.com/ocf/ocfweb/edit/master/ocfweb/docs/docs' +
            self.name +
            '.md'
        )

    @cached_property
    def history_url(self):
        """Return a GitHub history URL for this page."""
        return (
            'https://github.com/ocf/ocfweb/commits/master/ocfweb/docs/docs' +
            self.name +
            '.md'
        )
