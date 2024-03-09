.. _Update Guide:

Update Visualization Guide
==========================

`Observable Plot <https://observablehq.com/plot/>`_ does not offer an easy way to update dynamically the visualization. Currently, the only way for updating a :code:`Plot` is by `following this example <https://observablehq.com/@fil/plot-animate-a-bar-chart/2>`_.
However, it only works on the platform Observable because you won't be able to access :code:`Plot.update` outside Observable.

Therefore, if you want to update your visualization, you must use `d3js <https://d3js.org/>`_.

Example
-------

The goal of this example is to update a sine wave by adding new values.

First we create a :code:`Script` class :

.. code:: python

    from math import sin, pi

    from detroit import Script, d3, svg, function
    from detroit import js, Data, arrange # useful classes to simplify js syntax 
    from detroit import websocket_render  # function to render and update values
    from collections import namedtuple

    Margin = namedtuple("Margin", ("top", "right", "bottom", "left"))

    # Optional : Initial data
    istep = 4 * pi / 1000
    xv = [istep * i for i in range(1000)]
    yv = list(map(sin, xv))
    data = Data.arrange([xv, yv])
    # else you can do
    # data = Data([])

    margin = Margin(10, 30, 30, 60)
    width = 660 - margin.left - margin.right
    height = 420 - margin.top - margin.bottom

    script = Script()

    script(
        "svg",
        d3.select(script.plot_id)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", f"translate({margin.left}, {margin.top})"),
    )
    x = script("x", d3.scaleLinear().domain([0, max(xv)]).range([0, width]))

    script(
        svg.append("g")
        .attr("transform", f"translate(0, {height / 2})")
        .attr("class", "xaxis")
        .call(d3.axisBottom(x))
    )
    y = script("y", d3.scaleLinear().domain([-1, 1]).range([height, -1]).nice())

    script(svg.append("g").call(d3.axisLeft(y)))

    line = script("line",
        svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "deepskyblue")
        .attr("d", d3.line()
          .x(function("d").inline("x(d.x)"))
          .y(function("d").inline("y(d.y)"))
        )
    )

Then we add a function to update our values in our plot :

.. code:: python

    # Create `function update(data, xmax){...}` in javascript
    update = function("data", "xmax", name="update")

    # Replace the word "d3" by "x" and
    # update the domain given the `xmax` value
    update(d3(content="x").domain([0, js("xmax")]).nice())
    update(svg.selectAll("g.xaxis").call(d3.axisBottom(x)))

    # Replace the word "svg" by "line" and
    # update new data
    update(
        svg(content="line").datum(data)
          .attr("d", d3.line()
          .x(function("d").inline("x(d.x)"))
          .y(function("d").inline("y(d.y)"))
        )
    )

    # Add the update function to the script
    script(update)

Then you must send new data through a generator :

.. code:: python

    def generator():
        s = 1000
        istep = 4 * pi / 1000
        xv = [istep * i for i in range(1000)]
        yv = list(map(sin, xv))
        for i in range(1000):
            xmax = istep * (s + i)
            xv.append(xmax)
            yv.append(sin(istep * (s + i)))
            yield {"values": arrange([xv, yv]), "xmax": xmax}

Finally, you must inform how your plot must be updated :

.. code:: python

    event = js("update(received_data.values, received_data.xmax);")

    websocket_render(
      generator,
      script,
      event=event,
      init_data=data, # optional
    )
