import io
from textwrap import dedent

import mock
import pytest

import ocfweb.component.markdown
from ocfweb.component.markdown import markdown_and_toc
from ocfweb.component.markdown import text_and_meta


def assert_markdown(content, expected_html, expected_toc=None):
    html, toc = markdown_and_toc(dedent(content))
    assert html.strip() == dedent(expected_html).strip()

    if expected_toc is not None:
        assert toc == expected_toc


def test_simple_markdown():
    assert_markdown(
        '''\
            # this is an h1

            this is some paragraph text

            * bullet
            * bullet 2
        ''',
        '''\
            <h1 id="h1_this-is-an-h1">this is an h1 <a class="anchor" href="#h1_this-is-an-h1"><span></span></a></h1>
            <p>this is some paragraph text</p>
            <ul>
            <li>bullet</li>
            <li>bullet 2</li>
            </ul>
        '''
    )


def test_comments_get_stripped():
    assert_markdown(
        '''\
            this is some paragraph text

            <!-- ignore this please -->

            also <!-- ignore this --> lol
        ''',
        '''\
            <p>this is some paragraph text</p>
            <p>also  lol</p>
        '''
    )


@pytest.mark.parametrize('language', ('python', 'asdf', ''))
def test_code_rendering(language):
    with mock.patch.object(
            ocfweb.component.markdown,
            'highlight',
            return_value='<this would be code>\n',
    ):
        assert_markdown(
            '''\
                this is some paragraph text

                ```{language}
                def hello(world):
                    print('sup')
                ```

                yup
            '''.format(language=language),
            '''\
                <p>this is some paragraph text</p>
                <this would be code>
                <p>yup</p>
            '''
        )


def test_django_links():
    assert_markdown(
        '''\
            this is [[a link|staff-hours]]

            this is [[a link with a fragment|staff-hours#yolo]]
        ''',
        '''\
            <p>this is <a href="/staff-hours">a link</a></p>
            <p>this is <a href="/staff-hours#yolo">a link with a fragment</a></p>
        '''
    )


def test_header_default_id():
    assert_markdown(
        '''\
            # this is an h1
        ''',
        '''\
            <h1 id="h1_this-is-an-h1">this is an h1 <a class="anchor" href="#h1_this-is-an-h1"><span></span></a></h1>
        '''
    )


def test_header_custom_id():
    assert_markdown(
        '''\
            ### this is an h3    {something-here}
        ''',
        '''\
            <h3 id="something-here">this is an h3 <a class="anchor" href="#something-here"><span></span></a></h3>
        '''
    )


def test_header_with_collision_automatic():
    assert_markdown(
        '''\
            # this is an h1
            # this is an h1
        ''',
        '''\
            <h1 id="h1_this-is-an-h1">this is an h1 <a class="anchor" href="#h1_this-is-an-h1"><span></span></a></h1>
            <h1 id="h1_this-is-an-h1_">this is an h1 <a class="anchor" href="#h1_this-is-an-h1_"><span></span></a></h1>
        '''
    )


def test_header_with_collision_manual():
    with pytest.raises(ValueError):
        assert_markdown(
            '''\
                # this is an h1    {lol}
                # this is an h1    {lol}
            ''',
            None,
        )


def test_table_of_contents():
    assert_markdown(
        '''\
            # this is an h1    {h1}
            ## this is an h2    {h2}

            hello world

            ### this is an h3    {h3}
            ## this is another h2    {h2-again}

            sup
        ''',
        '''\
            <h1 id="h1">this is an h1 <a class="anchor" href="#h1"><span></span></a></h1>
            <h2 id="h2">this is an h2 <a class="anchor" href="#h2"><span></span></a></h2>
            <p>hello world</p>
            <h3 id="h3">this is an h3 <a class="anchor" href="#h3"><span></span></a></h3>
            <h2 id="h2-again">this is another h2 <a class="anchor" href="#h2-again"><span></span></a></h2>
            <p>sup</p>
        ''',
        [
            (1, 'this is an h1', 'h1'),
            (2, 'this is an h2', 'h2'),
            (3, 'this is an h3', 'h3'),
            (2, 'this is another h2', 'h2-again'),
        ],
    )


def test_text_and_meta():
    text, meta = text_and_meta(
        io.StringIO('''
        [[!meta title="Frequently asked questions"]]
        [[!meta herp="derp"]]
        hello world
        '''),
    )

    assert text.strip() == 'hello world'
    assert meta == {
        'title': 'Frequently asked questions',
        'herp': 'derp',
    }
