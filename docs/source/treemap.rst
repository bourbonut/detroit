Treemap chart
=============

.. image:: figures/light-treemap.svg
   :align: center
   :class: only-light

.. image:: figures/dark-treemap.svg
   :align: center
   :class: only-dark

1. Load data

.. code:: python

   # Source: https://observablehq.com/@d3/treemap/2
   import detroit as d3
   import json
   import requests
   import re

   URL = (
       "https://static.observableusercontent.com/files/e65374209781891f37dea1e7a6e1c5e020a"
       "3009b8aedf113b4c80942018887a1176ad4945cf14444603ff91d3da371b3b0d72419fa8d2ee0f6e81"
       "5732475d5de?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27flare"
       "-2.json"
   )

   data = json.loads(requests.get(URL).content)

2. Make the treemap chart

.. code:: python

   width = 1154
   height = 1154

   color = d3.scale_ordinal([d["name"] for d in data["children"]], d3.SCHEME_TABLEAU_10)

   # Transform data into hierarchical structure and organize it as treemap
   root = (
       d3.treemap()
       .set_tile(d3.treemap_binary)
       .set_size([width, height])
       .set_padding(1)
       .set_round(True)
   )(d3.hierarchy(data).sum(lambda d: d.get("value")).sort(lambda d: -d.value))

   # Create a SVG container
   svg = (
       d3.create("svg")
       .attr("viewBox", [0, 0, width, height])
       .attr("width", width)
       .attr("height", height)
       .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;")
   )

   # Create leaf groups
   leaf = (
       svg.select_all("g")
       .data(root.leaves())
       .join("g")
       .attr("transform", lambda d: f"translate({d.x0}, {d.y0})")
   )

   format_func = d3.format(",d")


   def title(node):
       names = ".".join((d.data["name"] for d in reversed(node.ancestors())))
       return f"{names}\n{format_func(node.value)}"


   leaf.append("title").text(title)

   leaf_index = 1


   def leaf_uid(node, i):
       global leaf_index
       id_value = node.leaf_uid = f"O-leaf-{leaf_index}"
       leaf_index += 1
       return id_value


   def fill(d):
       while d.depth > 1:
           d = d.parent
       return color(d.data["name"])


   # Add leaves as rectangle
   (
       leaf.append("rect")
       .attr("id", leaf_uid)
       .attr("fill", fill)
       .attr("fill-opacity", 0.6)
       .attr("width", lambda d: d.x1 - d.x0)
       .attr("height", lambda d: d.y1 - d.y0)
   )

   clip_index = 1


   def clip_uid(node):
       global clip_index
       id_value = node.clip_uid = f"O-clip-{clip_index}"
       clip_index += 1
       return id_value


   # Add clip path to avoid overlaps
   (
       leaf.append("clipPath")
       .attr("id", clip_uid)
       .append("use")
       .attr("xlink:href", lambda d: f"#{d.leaf_uid}")
   )

   # Add text for each leaf
   (
       leaf.append("text")
       .attr("clip-path", lambda d: f"url(#{d.clip_uid})")
       .select_all("tspan")
       .data(
           lambda _, d: [x for x in re.split(r"(?=[A-Z][a-z])|\s+", d.data["name"]) if x]
           + [format_func(d.value)]
       )
       .join("tspan")
       .attr("x", 3)
       .attr("y", lambda d, i, nodes: f"{(i == len(nodes) - 1) * 0.3 + 1.1 + i * 0.9}em")
       .attr("fill-opacity", lambda d, i, nodes: 0.7 if i == len(nodes) - 1 else None)
       .text(lambda d: d)
   )

3. Save your chart

.. code:: python

   with open("treemap.svg", "w") as file:
       file.write(str(svg))
