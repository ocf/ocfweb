import mock
import pytest

from ocfweb.caching import _make_function_call_key
from ocfweb.caching import _make_key
from ocfweb.caching import cache
from ocfweb.caching import cache_lookup_with_fallback
from ocfweb.caching import periodic


class TestCacheLookupWithFallback:

    def test_evaluates_fallback_on_miss(self):
        """Ensure that if we miss, we call the fallback."""
        fallback = mock.Mock(return_value='asdf')
        result = cache_lookup_with_fallback('key', fallback)
        fallback.assert_called_once_with()
        assert result == fallback.return_value

    def test_uses_cache_on_hit(self):
        """Ensure that we actually do use the cache when available."""
        # put it in the cache
        fallback = mock.Mock(return_value='asdf')
        cache_lookup_with_fallback('key', fallback)
        fallback.assert_called_once_with()

        # retrieve from cache
        fallback2 = mock.Mock(return_value='gggg')
        result = cache_lookup_with_fallback('key', fallback2)
        fallback2.assert_not_called()
        assert result == fallback.return_value


class TestCacheDecorator:

    def test_evaluates_function_on_miss(self):
        """Ensure that if we miss, we call the function."""
        m = mock.Mock(__name__='name', return_value='boop')
        fn = cache()(m)
        assert fn() == m.return_value
        m.assert_called_once_with()

    def test_evaluates_function_on_miss_with_args(self):
        """Ensure that if we miss, we call the function (and include args)."""
        m = mock.Mock(__name__='name', side_effect=lambda x, y: (x, y))
        fn = cache()(m)
        assert fn('herp', 'derp') == ('herp', 'derp')
        m.assert_called_once_with('herp', 'derp')

    def test_uses_cache_on_hit(self):
        """Ensure that we actually do use the cache when available."""
        # put it in the cache
        m = mock.Mock(__name__='name', return_value='boop')
        fn = cache()(m)
        fn()
        m.assert_called_once_with()

        # retrieve it from the cache
        m.side_effect = lambda: 1 / 0  # in case it gets evaluated again...
        result = fn()
        assert result == m.return_value
        assert m.call_count == 1

    def test_different_args_cached_separately(self):
        """Ensure that we properly include arguments in the cache key."""
        # put two different keys in the cache for the same function
        m = mock.Mock(__name__='name', side_effect=lambda x, y: (x, y))
        fn = cache()(m)
        fn('herp', 'derp')
        fn('beep', 'boop')
        m.assert_has_calls([mock.call('herp', 'derp'), mock.call('beep', 'boop')])

        # retrieve it from the cache
        m.side_effect = lambda x, y: 1 / 0  # in case it gets evaluated again...
        assert fn('herp', 'derp') == ('herp', 'derp')
        assert fn('beep', 'boop') == ('beep', 'boop')

        assert m.call_count == 2

        # make sure it still passes through
        with pytest.raises(ZeroDivisionError):
            fn('anything', 'else')

    def test_different_functions_cached_separately(self):
        """Ensure that we properly include function names in the cache key."""
        # put one key in the cache for two different functions
        m1 = mock.Mock(__name__='name', side_effect=lambda x, y: (x, y))
        m2 = mock.Mock(__name__='name2', side_effect=lambda x, y: (y, x))
        fn1 = cache()(m1)
        fn2 = cache()(m2)
        fn1('herp', 'derp')
        fn2('herp', 'derp')

        m1.assert_called_once_with('herp', 'derp')
        m2.assert_called_once_with('herp', 'derp')

        # retrieve both from the cache
        m1.side_effect = lambda x, y: 1 / 0  # in case it gets evaluated again...
        m2.side_effect = lambda x, y: 1 / 0  # in case it gets evaluated again...

        assert fn1('herp', 'derp') == ('herp', 'derp')
        assert fn2('herp', 'derp') == ('derp', 'herp')

        assert m1.call_count == 1
        assert m2.call_count == 1


@pytest.yield_fixture
def mock_ocfweb_version():
    with mock.patch('ocfweb.caching.ocfweb_version') as m:
        yield m.return_value


class TestCacheKeys:

    def test_make_key(self, mock_ocfweb_version):
        assert _make_key([]) == (mock_ocfweb_version,)
        assert _make_key(()) == (mock_ocfweb_version,)

        assert _make_key(['hello', 'world']) == (mock_ocfweb_version, 'hello', 'world')
        assert _make_key(('hello', 'world')) == (mock_ocfweb_version, 'hello', 'world')

    def test_make_function_call_key(self, mock_ocfweb_version):
        key = 'ocfweb.caching#_make_function_call_key'

        assert _make_function_call_key(
            _make_function_call_key,
            (),
            {},
        ) == (mock_ocfweb_version, key, (), ())

        assert _make_function_call_key(
            _make_function_call_key,
            ('herp', 'derp'),
            {},
        ) == (mock_ocfweb_version, key, ('herp', 'derp'), ())

        assert _make_function_call_key(
            _make_function_call_key,
            ('herp', 'derp'),
            {'c': 'd', 'a': 'b'},
        ) == (mock_ocfweb_version, key, ('herp', 'derp'), (('a', 'b'), ('c', 'd')))


class TestPeriodicDecorator:

    def test_evaluates_function_on_miss(self):
        """Ensure that if we miss, we call the function."""
        m = mock.Mock(__name__='name', return_value='boop')
        fn = periodic(60)(m)
        assert fn() == m.return_value
        m.assert_called_once_with()

    def test_uses_cache_on_hit(self):
        """Ensure that we actually do use the cache when available."""
        # put it in the cache
        m = mock.Mock(__name__='name', return_value='boop')
        fn = periodic(60)(m)
        fn()
        m.assert_called_once_with()

        # retrieve it from the cache
        m.side_effect = lambda: 1 / 0  # in case it gets evaluated again...
        result = fn()
        assert result == m.return_value
        assert m.call_count == 1

    def test_different_functions_cached_separately(self):
        """Ensure that we properly include function names in the cache key."""
        # put one key in the cache for two different functions
        m1 = mock.Mock(__name__='name', return_value='herp')
        m2 = mock.Mock(__name__='name2', return_value='derp')
        fn1 = periodic(60)(m1)
        fn2 = periodic(60)(m2)
        fn1()
        fn2()

        assert m1.call_count == 1
        assert m2.call_count == 1

        # retrieve both from the cache
        m1.side_effect = lambda x, y: 1 / 0  # in case it gets evaluated again...
        m2.side_effect = lambda x, y: 1 / 0  # in case it gets evaluated again...

        assert fn1() == 'herp'
        assert fn2() == 'derp'

        assert m1.call_count == 1
        assert m2.call_count == 1
