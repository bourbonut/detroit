Pack chart
==========

.. image:: figures/light-pack.svg
   :align: center
   :class: only-light

.. image:: figures/dark-pack.svg
   :align: center
   :class: only-dark

1. Load data

.. code:: python

   # Source: https://observablehq.com/@d3/tree-component
   import detroit as d3
   import json
   import requests
   import re
   from uuid import uuid4

   # Load data
   URL = (
       "https://static.observableusercontent.com/files/e65374209781891f37dea1e7a6e1c5e020a"
       "3009b8aedf113b4c80942018887a1176ad4945cf14444603ff91d3da371b3b0d72419fa8d2ee0f6e81"
       "5732475d5de?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27flare"
       "-2.json"
   )

   flare = json.loads(requests.get(URL).content)

2. Make the pack chart

.. code:: python

   def label(d, n):
       return "\n".join(re.split(r"(?=[A-Z][a-z])", d["name"]) + [str(n.value)])


   def title(d, n):
       names = ".".join((node.data["name"] for node in reversed(n.ancestors())))
       return f"{names}\n{n.value}"


   def link(d, n):
       p1 = "tree" if n.children else "blob"
       p2 = "/".join((node.data["name"] for node in reversed(n.ancestors())))
       p3 = "" if n.children else ".as"
       return f"https://github.com/prefuse/Flare/{p1}/master/flare/src/{p2}{p3}"


   width = 1152
   height = 1152

   # Transform data into hierarchical structure
   root = d3.hierarchy(flare).sum(lambda d: max(0, d.get("value") or 0))

   descendants = root.descendants()
   leaves = list(filter(lambda d: not d.children, descendants))
   for i, leave in enumerate(leaves):
       leave.index = i

   labels = [label(d.data, d) for d in leaves]
   titles = [title(d.data, d) for d in descendants]

   root.sort(lambda d: -d.value)

   # Orginize data as pack structure
   d3.pack().set_size([width - 2, height - 2]).set_padding(3)(root)

   # Create SVG container
   svg = (
       d3.create("svg")
       .attr("viewBox", [-1, -1, width, height])
       .attr("width", width)
       .attr("height", height)
       .attr("style", "max-width: 100%; height: auto;")
       .attr("font-family", "sans-serif")
       .attr("font-size", 10)
       .attr("text-anchor", "middle")
   )

   # Make nodes as links
   node = (
       svg.select_all("a")
       .data(descendants)
       .join("a")
       .attr("xlink:href", lambda d: link(d.data, d))
       .attr("target", "_blank")
       .attr("transform", lambda d: f"translate({d.x}, {d.y})")
   )

   # Add circles into nodes
   (
       node.append("circle")
       .attr("fill", lambda d: "#fff" if d.children else "#ddd")
       .attr("stroke", lambda d: "#bbb" if d.children else None)
       .attr("r", lambda d: d.r)
   )

   node.append("title").text(lambda d, i: titles[i])

   uid = f"O-{uuid4().hex[:16]}"
   # Make leaves
   leaf = node.filter(
       lambda d: not d.children and d.r > 10 and labels[d.index] is not None
   )
   # Add clip path and circles
   (
       leaf.append("clipPath")
       .attr("id", lambda d: f"{uid}-clip-{d.index}")
       .append("circle")
       .attr("r", lambda d: d.r)
   )

   (
       leaf.append("text")
       .attr("clip-path", lambda d: f"url(#{uid}-clip-{d.index})")
       .select_all("tspan")
       .data(lambda _, d: [x for x in re.split(r"\n", f"{labels[d.index]}") if x])
       .join("tspan")
       .attr("x", 0)
       .attr("y", lambda d, i, D: f"{(i - len(D) * 0.5) + 0.85}em")
       .attr("fill-opacity", lambda d, i, D: 0.7 if i == len(D) - 1 else None)
       .text(lambda d: d)
   )

3. Save your chart

.. code:: python

   with open("pack.svg", "w") as file:
       file.write(str(svg))
