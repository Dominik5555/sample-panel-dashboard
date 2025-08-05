import matplotlib.pyplot as plt
import numpy as np
import panel as pn

pn.extension(design="material")  # minimal load, good style

# Widgets
freq = pn.widgets.FloatSlider(name='Frequency', start=1, end=10, step=0.1, value=2)
amp = pn.widgets.FloatSlider(name='Amplitude', start=0.1, end=5, step=0.1, value=1)

# Plotting function
def plot_sine(frequency, amplitude):
    x = np.linspace(0, 2 * np.pi, 500)
    y = amplitude * np.sin(frequency * x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(f'Sine Wave: {frequency:.1f} Hz, {amplitude:.1f}x')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    return fig

# Bind the function to the widgets
interactive_plot = pn.bind(plot_sine, freq, amp)

# Layout
dashboard = pn.Column(
    "# 🎛️ Interactive Sine Plot",
    pn.Row(freq, amp),
    pn.pane.Matplotlib(interactive_plot, tight=True),
)

dashboard.servable()
