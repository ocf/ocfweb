import io

from matplotlib.backends.backend_agg import FigureCanvasAgg


def plot_to_image_bytes(fig, format='svg', **kwargs):
    """Return bytes representing the plot image."""
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_figure(buf, format=format, **kwargs)
    return buf.getvalue()
