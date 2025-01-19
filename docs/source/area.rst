Area chart
==========

.. image:: figures/light-area.svg
   :align: center
   :class: only-light

.. image:: figures/dark-area.svg
   :align: center
   :class: only-dark

1. Load data

.. code:: python

   import detroit as d3
   import polars as pl # for data manipulation
   from collections import namedtuple

   URL = "https://static.observableusercontent.com/files/de259092d525c13bd10926eaf7add45b15f2771a8b39bc541a5bba1e0206add4880eb1d876be8df469328a85243b7d813a91feb8cc4966de582dc02e5f8609b7?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27aapl.csv"

   Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

   aapl = pl.read_csv(URL).select(
       pl.col("date").str.to_datetime("%Y-%m-%d"),
       pl.col("close"),
   )

.. code::

   shape: (1_280, 2)
   ┌─────────────────────┬────────┐
   │ date                ┆ close  │
   │ ---                 ┆ ---    │
   │ datetime[μs]        ┆ f64    │
   ╞═════════════════════╪════════╡
   │ 2007-04-23 00:00:00 ┆ 93.24  │
   │ 2007-04-24 00:00:00 ┆ 95.35  │
   │ 2007-04-25 00:00:00 ┆ 98.84  │
   │ 2007-04-26 00:00:00 ┆ 99.92  │
   │ 2007-04-29 00:00:00 ┆ 99.8   │
   │ …                   ┆ …      │
   │ 2012-04-24 00:00:00 ┆ 610.0  │
   │ 2012-04-25 00:00:00 ┆ 607.7  │
   │ 2012-04-26 00:00:00 ┆ 603.0  │
   │ 2012-04-29 00:00:00 ┆ 583.98 │
   │ 2012-05-01 00:00:00 ┆ 582.13 │
   └─────────────────────┴────────┘


2. Make the area chart

.. code:: python

   # Declare the chart dimensions and margins.
   width = 928
   height = 500
   margin = Margin(20, 30, 30, 40)

   # Declare the x (horizontal position) scale.
   x = d3.scale_time(
       [aapl["date"].min(), aapl["date"].max()], [margin.left, width - margin.right]
   )

   # # Declare the y (vertical position) scale.
   y = d3.scale_linear([0, aapl["close"].max()], [height - margin.bottom, margin.top])

   # Declare the area generator.
   area = d3.area().x(lambda d: x(d[0].timestamp())).y0(y(0)).y1(lambda d: y(d[1]))

   # Create the SVG container.
   svg = (
       d3.create("svg")
       .attr("width", width)
       .attr("height", height)
       .attr("viewBox", f"0 0 {width} {height}")
       .attr("style", "max-width: 100%; height: auto;")
   )

   # Append a path for the area (under the axes).
   svg.append("path").attr("fill", "steelblue").attr("d", area(aapl.iter_rows()))

   # Add the x-axis.
   svg.append("g").attr("transform", f"translate(0, {height - margin.bottom})").call(
       d3.axis_bottom(x).set_ticks(width / 80).set_tick_size_outer(0)
   )

   # Add the y-axis, remove the domain line, add grid lines and a label.
   (
       svg.append("g")
       .attr("transform", f"translate({margin.left}, 0)")
       .call(d3.axis_left(y).set_ticks(height / 40))
       .call(lambda g: g.select(".domain").remove())
       .call(
           lambda g: g.select_all(".tick")
           .select_all("line")
           .clone()
           .attr("x2", width - margin.left - margin.right)
           .attr("stroke-opacity", 0.1)
       )
       .call(
           lambda g: (
               g.append("text")
               .attr("x", -margin.left)
               .attr("y", 10)
               .attr("fill", "currentColor")
               .attr("text-anchor", "start")
               .text("↑ Daily close ($)")
           )
       )
   )

3. Save your chart

.. code:: python

   with open("area.svg", "w") as file:
       file.write(str(svg))
