import numpy as np
import pandas as pd
import panel as pn
from bokeh.plotting import figure

pn.extension(design="material")  # light default, small payload

# -----------------------
# Widgets (in the sidebar)
# -----------------------
freq = pn.widgets.FloatSlider(name="Sine frequency", start=0.1, end=5.0, step=0.1, value=1.0)
npoints = pn.widgets.IntSlider(name="Points", start=100, end=2000, step=100, value=500)
noise = pn.widgets.Checkbox(name="Add noise", value=True)

genres_all = ["Rock", "Pop", "Hip-Hop", "Electronic", "Jazz", "Metal", "Folk", "Classical"]
genres = pn.widgets.MultiChoice(name="Genres to show", options=genres_all, value=["Rock", "Pop", "Hip-Hop", "Electronic"])

# -----------------------
# Reactive data builders
# -----------------------
@pn.cache  # cache across reruns in same process
def base_genre_df(seed=42):
    rng = np.random.default_rng(seed)
    counts = rng.integers(200, 2000, size=len(genres_all))
    trend = rng.normal(0, 1, size=len(genres_all))
    df = pd.DataFrame({"genre": genres_all, "count": counts, "trend_z": trend})
    return df.sort_values("count", ascending=False)

def make_sine(freq_val, npoints_val, noise_on):
    x = np.linspace(0, 2*np.pi, npoints_val)
    y = np.sin(freq_val * x)
    if noise_on:
        y = y + 0.15*np.random.default_rng(0).normal(size=len(x))
    p = figure(height=300, sizing_mode="stretch_width", title="Sine Wave")
    p.line(x, y, line_width=2)
    p.xaxis.axis_label = "x"
    p.yaxis.axis_label = "sin(f·x)"
    return p

def make_bar(selected_genres):
    df = base_genre_df()
    if selected_genres:
        df = df[df["genre"].isin(selected_genres)]
    p = figure(x_range=list(df["genre"]), height=300, sizing_mode="stretch_width",
               title="Plays per Genre (synthetic)")
    p.vbar(x="genre", top="count", width=0.8, source=df)
    p.xaxis.major_label_orientation = 0.8
    p.yaxis.axis_label = "Count"
    return p

def make_summary(selected_genres, nrows=5):
    df = base_genre_df()
    total = int(df["count"].sum())
    sel_total = int(df[df["genre"].isin(selected_genres)]["count"].sum()) if selected_genres else total
    top = df.head(nrows)[["genre", "count"]]
    md = f"""### Overview
- **Total plays (all genres):** {total:,}
- **Total plays (selected):** {sel_total:,}
- **# Genres selected:** {len(selected_genres) if selected_genres else len(genres_all)}"""
    return pn.Column(pn.pane.Markdown(md), pn.pane.DataFrame(top, index=False, height=160))

# -----------------------
# Bind plots to widgets
# -----------------------
sine_panel = pn.bind(make_sine, freq_val=freq, npoints_val=npoints, noise_on=noise)
bar_panel  = pn.bind(make_bar, selected_genres=genres)
summary    = pn.bind(make_summary, selected_genres=genres)

# -----------------------
# Template layout
# -----------------------
tmpl = pn.template.FastListTemplate(
    title="Sample Panel Dashboard",
    sidebar=[pn.pane.Markdown("## Controls"), freq, npoints, noise, pn.layout.Divider(), genres],
    main=[
        pn.Row(sine_panel),
        pn.Row(bar_panel),
        pn.Card(summary, title="Summary", collapsible=False),
    ],
    sidebar_width=300
)

tmpl.servable()
