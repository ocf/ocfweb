import io
import urllib.parse
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import Optional
from typing import Tuple

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

MIN_DAYS = 1
MAX_DAYS = 365 * 5
DEFAULT_DAYS = 14


def current_start_end() -> Tuple[date, date]:
    """Return current default start and end date."""
    end = date.today()
    return end - timedelta(days=DEFAULT_DAYS), end


def canonical_graph(
    hot_path: Optional[Callable[..., Any]] = None,
    default_start_end: Callable[..., Tuple[date, date]] = current_start_end,
) -> Callable[..., Any]:
    """Decorator to make graphs with a start_day and end_day.

    It does three primary things:

    1. Redirects to the current "start_day" or "end_day" if one (or both) is
       missing.

    2. Makes sure the "start_day" and "end_day" in the query string is
       canonical, redirecting if necessary. For example, "2016-08-01" and
       "2016-8-1" are both the same date, but we don't want two duplicate URLs.

    3. If "start_day" and "end_day" are the current defaults, it calls the
       optional "hot_path" argument, which is a function which takes no
       arguments (presumably cached or periodic) and returns the current
       default graph.

    :param hot_path: optional, function to call (default: None)
    :param default_start_end: optional, function to get current start/end date
                              (default: current_start_end)
    """
    def decorator(fn: Callable[[Any, date, date], Any]) -> Callable[[Any], Any]:
        def wrapper(request: Any) -> Any:
            def _day_from_params(param: str, default: date) -> date:
                try:
                    return datetime.strptime(request.GET.get(param, ''), '%Y-%m-%d').date()
                except ValueError:
                    return default

            default_start, default_end = default_start_end()

            start_day = _day_from_params('start', default_start)
            end_day = _day_from_params('end', default_end)

            if end_day <= start_day:
                return HttpResponse(
                    'end_day must be after start_day',
                    status=400,
                )

            # redirect to canonical url
            if (
                    request.GET.get('start') != start_day.isoformat() or
                    request.GET.get('end') != end_day.isoformat()
            ):
                return redirect(
                    '{}?{}'.format(
                        reverse(request.resolver_match.url_name),
                        urllib.parse.urlencode({
                            'start': start_day.isoformat(),
                            'end': end_day.isoformat(),
                        }),
                    ),
                )

            if hot_path and start_day == default_start and end_day == default_end:
                return hot_path()
            else:
                return fn(request, start_day, end_day)

        return wrapper
    return decorator


def plot_to_image_bytes(fig: Figure, format: str = 'svg', **kwargs: Any) -> bytes:
    """Return bytes representing the plot image."""
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_figure(buf, format=format, **kwargs)
    return buf.getvalue()
