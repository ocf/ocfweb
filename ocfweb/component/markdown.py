import re

import mistune
from django.core.urlresolvers import reverse

# tags of a format like: [[!meta title="Backups"]]
META_REGEX = re.compile('\[\[!meta ([a-z]+)="([^"]*)"\]\]')


class HtmlCommentsInlineLexerMixin:
    """Strip HTML comments inside lines."""

    def enable_html_comments(self):
        self.rules.html_comment = re.compile(
            '^<!--(.*?)-->'
        )
        self.default_rules.insert(0, 'html_comment')

    def output_html_comment(self, m):
        return ''


class HtmlCommentsBlockLexerMixin:
    """Strip blocks which consist entirely of HTML comments."""

    def enable_html_comments(self):
        self.rules.html_comment = re.compile(
            '^<!--(.*?)-->'
        )
        self.default_rules.insert(0, 'html_comment')

    def parse_html_comment(self, m):
        pass


class DjangoLinkInlineLexerMixin:
    """Turn special Markdown link syntax into Django links.

    In Django templates, we can use `url` tags, such as:
        {% url 'staff-hours' %}
        {% url 'doc' 'staff/backend/backups' %}

    In Markdown, we use the following fake syntax to generate Django links:
        [[human readable name|staff-hours]]
        [[human readable name|doc staff/backend/backups]]

    You can link to fragments with a # at the very end:
        [[human readable name|staff-hours#something]]
        [[human readable name|doc staff/backend/backups#something]]
    """

    split_words = re.compile('((?:\S|\\\\ )+)')

    def enable_django_links(self):
        self.rules.django_link = re.compile(
            '^\[\[(?!\!)'
            '([\s\S]+?)'
            '\|'
            '([^#]+?)'
            '(?:#(.*?))?'
            '\]\]'
        )
        self.default_rules.insert(0, 'django_link')

    def output_django_link(self, m):
        text, target, fragment = m.group(1), m.group(2), m.group(3)

        def href(link, fragment):
            if fragment:
                return link + '#' + fragment
            return link

        words = DjangoLinkInlineLexerMixin.split_words.findall(target)
        name, *params = words
        return self.renderer.link(
            link=href(reverse(name, args=params), fragment),
            title=None,
            text=text,
        )


class TableOfContentsRendererMixin:

    def reset_toc(self):
        self.toc = []
        self.toc_ids = set()

    def get_toc(self):
        return self.toc

    def header(self, text, level, raw=None):
        id = 'h{level}_{title}'.format(
            level=level,
            title=re.sub('[^a-z0-9\-_ ]', '', text.lower()).strip().replace(' ', '-'),
        )

        # dumb collision avoidance
        while id in self.toc_ids:
            id += '_'

        self.toc.append((level, text, id))
        self.toc_ids.add(id)
        return '<h{level} id="{id}">{text} <a class="" href="#{id}"><span></span></a></h{level}>\n'.format(
            level=level,
            id=id,
            text=text,
        )


class OcfMarkdownRenderer(
    TableOfContentsRendererMixin,
    mistune.Renderer,
):
    pass


class OcfMarkdownInlineLexer(
    mistune.InlineLexer,
    DjangoLinkInlineLexerMixin,
    HtmlCommentsInlineLexerMixin,
):
    pass


class OcfMarkdownBlockLexer(
    mistune.BlockLexer,
    HtmlCommentsBlockLexerMixin,
):
    pass


_renderer = OcfMarkdownRenderer(
    escape=True,
    hard_wrap=False,
)

_inline = OcfMarkdownInlineLexer(_renderer)
_inline.enable_html_comments()
_inline.enable_django_links()

_block = OcfMarkdownBlockLexer(mistune.BlockGrammar())
_block.enable_html_comments()

_markdown = mistune.Markdown(
    renderer=_renderer,
    inline=_inline,
    block=_block,
)


def markdown(text):
    _renderer.reset_toc()
    return _markdown(text)


def get_meta_tags(text):
    """Return tuple (text, meta dict) for the given text.

    Meta tags are stripped from the Markdown source, but the Markdown is
    not rendered.
    """
    meta = {}

    def repl(match):
        meta[match.group(1)] = match.group(2)
        return ''

    text = META_REGEX.sub(repl, text)
    return text, meta


def markdown_and_meta(text):
    """Return tuple (html, meta dict) for the given text."""
    text, meta = get_meta_tags(text)
    html = markdown(text)
    meta['toc'] = _renderer.get_toc()
    return html, meta
