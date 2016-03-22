import re

import mistune
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

from ocfweb.caching import cache

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


class CodeRendererMixin:
    """Render highlighted code."""
    # TODO: don't use inline styles; see http://pygments.org/docs/formatters/
    html_formatter = HtmlFormatter(noclasses=True)

    def block_code(self, code, lang):
        try:
            if lang:
                lexer = get_lexer_by_name(lang, stripall=True)
            else:
                lexer = guess_lexer(code)
        except ClassNotFound:
            lexer = get_lexer_by_name('shell')

        return highlight(code, lexer, CodeRendererMixin.html_formatter)


class DjangoLinkInlineLexerMixin:
    """Turn special Markdown link syntax into Django links.

    In Django templates, we can use `url` tags, such as:
        {% url 'staff-hours' %}
        {% url 'help' 'staff/backend/backups' %}

    In Markdown, we use the following fake syntax to generate Django links:
        [[human readable name|staff-hours]]
        [[human readable name|help staff/backend/backups]]

    You can link to fragments with a # at the very end:
        [[human readable name|staff-hours#something]]
        [[human readable name|help staff/backend/backups#something]]
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


class HeaderRendererMixin:
    """Mixin to render headers with auto-generated IDs (or provided IDs).

    If headers are written as usual, they'll be given automatically-generated
    IDs based on their header level and text.

    Headers can also be specified with an ID at the end wrapped in curly braces:

        ### My Header    {my_id}

    This ID will be used directly without further manipulation, and can be
    relied on for linking.

    Custom IDs can consist only of lowercase a-z, 0-9, dash, and underscore.

    IDs are tracked into a table of contents which should be reset before
    rendering a document and read afterwards.
    """

    def reset_toc(self):
        self.toc = []
        self.toc_ids = set()

    def get_toc(self):
        return self.toc

    def header(self, text, level, raw=None):
        custom_id_match = re.match(r'^(.*?)\s+{([a-z0-9\-_]+)}\s*$', text)
        if custom_id_match:
            text = custom_id_match.group(1)
            id = custom_id_match.group(2)

            if id in self.toc_ids:
                raise ValueError('Duplicate header ID in Markdown: "{}"'.format(id))
        else:
            id = 'h{level}_{title}'.format(
                level=level,
                title=re.sub('[^a-z0-9\-_ ]', '', strip_tags(text).lower()).strip().replace(' ', '-'),
            )

            # dumb collision avoidance
            while id in self.toc_ids:
                id += '_'

        self.toc.append((level, text, id))
        self.toc_ids.add(id)
        return '<h{level} id="{id}">{text} <a class="anchor" href="#{id}"><span></span></a></h{level}>\n'.format(
            level=level,
            id=id,
            text=text,
        )


class OcfMarkdownRenderer(
    HeaderRendererMixin,
    CodeRendererMixin,
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


def text_and_meta(f):
    """Return tuple (text, meta dict) for the given file.

    Meta tags are stripped from the Markdown source, but the Markdown is
    not rendered.
    """
    text = f.read()
    meta = {}

    def repl(match):
        meta[match.group(1)] = match.group(2)
        return ''

    text = META_REGEX.sub(repl, text)
    return text, meta


@cache()
def markdown_and_toc(text):
    """Return tuple (html, toc) for the given text."""
    html = markdown(text)
    return html, _renderer.get_toc()
