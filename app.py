import numpy as np
import panel as pn
from bokeh.plotting import figure

pn.extension(design="material")  # light default, small payload

# -----------------------
# Widgets
# -----------------------
freq = pn.widgets.FloatSlider(name="Frequency (f)", start=0.1, end=5.0, step=0.1, value=1.0)
amp  = pn.widgets.FloatSlider(name="Amplitude (A)", start=0.1, end=2.0, step=0.1, value=1.0)

# -----------------------
# Plot function
# -----------------------
def make_plot(f, a):
    x = np.linspace(0, 2*np.pi, 600)
    y = a * np.sin(f * x)
    p = figure(height=350, sizing_mode="stretch_width", title="y = A · sin(f · x)")
    p.line(x, y, line_width=2)
    p.xaxis.axis_label = "x"
    p.yaxis.axis_label = "y"
    return p

# -----------------------
# Bind (exact style you use)
# -----------------------
plot = pn.bind(make_plot, f=freq, a=amp)

# -----------------------
# Simple layout
# -----------------------
app = pn.Column(
    pn.pane.Markdown("## Simple Bound Plot (one figure, two sliders)"),
    pn.Row(freq, amp),
    plot,
    sizing_mode="stretch_width"
)

app.servable()
