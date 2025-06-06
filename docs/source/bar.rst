Bar chart
=========

.. image:: figures/light-bar.svg
   :align: center
   :class: only-light

.. image:: figures/dark-bar.svg
   :align: center
   :class: only-dark

1. Load data

.. code:: python

   # Source : https://observablehq.com/@d3/bar-chart/2
   import detroit as d3
   import polars as pl # for data manipulation
   from collections import namedtuple

   URL = "https://static.observableusercontent.com/files/09f63bb9ff086fef80717e2ea8c974f918a996d2bfa3d8773d3ae12753942c002d0dfab833d7bee1e0c9cd358cd3578c1cd0f9435595e76901508adc3964bbdc?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27alphabet.csv"
   Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

   alphabet = pl.read_csv(URL).sort(by="frequency", descending=True)

.. code::

   shape: (26, 2)
   ┌────────┬───────────┐
   │ letter ┆ frequency │
   │ ---    ┆ ---       │
   │ str    ┆ f64       │
   ╞════════╪═══════════╡
   │ E      ┆ 0.12702   │
   │ T      ┆ 0.09056   │
   │ A      ┆ 0.08167   │
   │ O      ┆ 0.07507   │
   │ I      ┆ 0.06966   │
   │ …      ┆ …         │
   │ K      ┆ 0.00772   │
   │ J      ┆ 0.00153   │
   │ X      ┆ 0.0015    │
   │ Q      ┆ 0.00095   │
   │ Z      ┆ 0.00074   │
   └────────┴───────────┘

2. Make the bar chart

.. code:: python

   width = 928
   height = 500
   margin = Margin(30, 0, 30, 40)

   # Declare the x (horizontal position) scale.
   # descending frequency
   x = (
       d3.scale_band()
       .set_domain(alphabet["letter"].unique(maintain_order=True))
       .set_range([margin.left, width - margin.right])
       .set_padding(0.1)
   )

   # Declare the y (vertical position) scale.
   y = (
       d3.scale_linear()
       .set_domain([0, alphabet["frequency"].max()])
       .set_range([height - margin.bottom, margin.top])
   )

   # Create the SVG container.
   svg = (
       d3.create("svg")
       .attr("width", width)
       .attr("height", height)
       .attr("viewBox", f"0 0 {width} {height}")
       .attr("style", "max-width: 100%; height: auto;")
   )

   # Add a rect for each bar.
   (
       svg.append("g")
       .select_all()
       .data(alphabet.iter_rows())
       .join("rect")
       .attr("x", lambda d: x(d[0]))
       .attr("y", lambda d: y(d[1]))
       .attr("height", lambda d: y(0) - y(d[1]))
       .attr("width", x.get_bandwidth())
       .attr("fill", "steelblue")
   )

   # Add the x-axis and label.
   svg.append("g").attr("transform", f"translate(0, {height - margin.bottom})").call(
       d3.axis_bottom(x).set_tick_size_outer(0)
   )

   # Add the y-axis and label, and remove the domain line.
   (
       svg.append("g")
       .attr("transform", f"translate({margin.left}, 0)")
       .call(d3.axis_left(y).set_tick_format(lambda y: str(int(y * 100))))
       .call(lambda g: g.select(".domain").remove())
       .call(
           lambda g: g.append("text")
           .attr("x", -margin.left)
           .attr("y", 10)
           .attr("fill", "currentColor")
           .attr("text-anchor", "start")
           .text("↑ Frequency (%)")
       )
   )

3. Save your chart

.. code:: python

   with open("bar.svg", "w") as file:
       file.write(str(svg))
