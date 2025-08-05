import panel as pn
pn.extension()

slider = pn.widgets.IntSlider(name="Slide me", start=0, end=100)
output = pn.bind(lambda x: f"You selected: {x}", slider)

pn.Column("# Sample Panel App", slider, output).servable()

