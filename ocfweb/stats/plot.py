import io


def plot_to_image_bytes(plt, format='svg', **kwargs):
    """Return bytes representing the plot image."""
    buf = io.BytesIO()
    plt.gcf().savefig(buf, format=format, **kwargs)
    buf.seek(0)
    return buf.read()
