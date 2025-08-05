import panel as pn
import numpy as np
from bokeh.plotting import figure

pn.extension()

# --- Title & Description ---
title = "# 🌍 Vanilla Dashboard"
description = pn.pane.Markdown("""
Welcome to your first Panel dashboard.  
This example shows two simple plots using synthetic data.
""")

# --- Plot 1: Line Plot ---
x = np.linspace(0, 10, 100)
y = np.sin(x)

plot1 = figure(title="Sine Wave", height=300, width=400)
plot1.line(x, y, line_width=2)

# --- Plot 2: Scatter Plot ---
x2 = np.random.rand(100)
y2 = np.random.rand(100)

plot2 = figure(title="Random Scatter", height=300, width=400)
plot2.circle(x2, y2, size=6, color="green", alpha=0.6)

# --- Layout ---
dashboard = pn.Column(
    title,
    description,
    pn.Row(plot1, plot2)
)

dashboard.servable()
