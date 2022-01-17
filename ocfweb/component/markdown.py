import re
from typing import Any
from typing import List
from typing import Match
from typing import Set
from typing import Tuple
from typing import TYPE_CHECKING

import mistune
from django.urls import reverse
from django.utils.html import strip_tags
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from ocfweb.caching import cache

# tags of a format like: [[!meta title="Backups"]]
META_REGEX = re.compile(r'---\n(?:(\w+): "((?:\w|\s)+)"\n)*---(?:\n|\s)*')

# Make mypy play nicely with mixins https://github.com/python/mypy/issues/5837
# TODO: issue has been resolved in mypy, patch when next version of mypy gets released
# More info: https://github.com/python/mypy/pull/7860


class MixinBase:
    def __init__(self, rules: Any, default_rules: Any) -> None:
        self.rules = rules
        self.default_rules = default_rules


_Base: Any = object
if TYPE_CHECKING:
    _Base = MixinBase


class HtmlCommentsLexerMixin(_Base):
    """Strip HTML comments as entire blocks or inside lines."""

    def enable_html_comments(self) -> None:
        self.rules.html_comment = re.compile(
            r'^<!--(.*?)-->',
        )
        self.default_rules.insert(0, 'html_comment')

    def output_html_comment(self, m: Match[Any]) -> str:
        return ''

    def parse_html_comment(self, m: Match[Any]) -> None:
        pass


class BackslashLineBreakLexerMixin(_Base):
    """Convert lines that end in a backslash into a simple line break.

    This follows GitHub-flavored Markdown on backslashes at the end of lines
    being treated as a hard line break
    (https://github.github.com/gfm/#backslash-escapes)

    For example, something like this (escaped for python's sake since this in
    in a string):

        This is a test\\
        with a line break

    would be rendered as:

        This is a test<br>
        with a line break
    """

    def enable_backslash_line_breaks(self) -> None:
        self.rules.backslash_line_break = re.compile(
            '^\\\\\n',
        )
        self.default_rules.insert(0, 'backslash_line_break')

    def output_backslash_line_break(self, m: Match[Any]) -> str:
        return '<br>'


class CodeRendererMixin(_Base):
    """Render highlighted code."""
    # TODO: don't use inline styles; see https://pygments.org/docs/formatters/
    html_formatter = HtmlFormatter(noclasses=True)

    def block_code(self, code: str, lang: str) -> str:
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
        else:
            lexer = get_lexer_by_name('text')

        return highlight(code, lexer, CodeRendererMixin.html_formatter)


class DjangoLinkInlineLexerMixin(_Base):
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

    split_words = re.compile(r'((?:\S|\\ )+)')

    def enable_django_links(self) -> None:
        self.rules.django_link = re.compile(
            r'^\[\[(?!\!)'
            r'([\s\S]+?)'
            r'\|'
            r'([^#]+?)'
            r'(?:#(.*?))?'
            r'\]\]',
        )
        self.default_rules.insert(0, 'django_link')

    def output_django_link(self, m: Match[Any]) -> str:
        text, target, fragment = m.group(1), m.group(2), m.group(3)

        def href(link: str, fragment: str) -> str:
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


class HeaderRendererMixin(_Base):
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

    def reset_toc(self) -> None:
        self.toc: List[Any] = []
        self.toc_ids: Set[Any] = set()

    def get_toc(self) -> List[Any]:
        return self.toc

    def header(self, text: str, level: int, raw: None = None) -> str:
        custom_id_match = re.match(r'^(.*?)\s+{([a-z0-9\-_]+)}\s*$', text)
        if custom_id_match:
            text = custom_id_match.group(1)
            id = custom_id_match.group(2)

            if id in self.toc_ids:
                raise ValueError(f'Duplicate header ID in Markdown: "{id}"')
        else:
            id = 'h{level}_{title}'.format(
                level=level,
                title=re.sub(r'[^a-z0-9\-_ ]', '', strip_tags(text).lower()).strip().replace(' ', '-'),
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
    HtmlCommentsLexerMixin,
    BackslashLineBreakLexerMixin,
):
    pass


class OcfMarkdownBlockLexer(
    mistune.BlockLexer,
    HtmlCommentsLexerMixin,
):
    pass


_renderer = OcfMarkdownRenderer(
    escape=True,
    hard_wrap=False,
)

_inline = OcfMarkdownInlineLexer(_renderer)
_inline.enable_html_comments()
_inline.enable_django_links()
_inline.enable_backslash_line_breaks()

_block = OcfMarkdownBlockLexer(mistune.BlockGrammar())
_block.enable_html_comments()

_markdown = mistune.Markdown(
    renderer=_renderer,
    inline=_inline,
    block=_block,
)


def markdown(text: str) -> mistune.Markdown:
    _renderer.reset_toc()
    return _markdown(text)


def text_and_meta(f: Any) -> Tuple[str, Any]:
    """Return tuple (text, meta dict) for the given file.

    Meta tags are stripped from the Markdown source, but the Markdown is
    not rendered.
    """
    text = f.read()
    meta = {}

    def repl(match: Match[Any]) -> str:
        meta[match.group(1)] = match.group(2)
        return ''

    text = META_REGEX.sub(repl, text)
    return text, meta


@cache()
def markdown_and_toc(text: str) -> Tuple[Any, Any]:
    """Return tuple (html, toc) for the given text."""
    html = markdown(text)
    return html, _renderer.get_toc()
