from collections import namedtuple

from cached_property import cached_property


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
