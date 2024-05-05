from detroit import js, render, save, d3, svg, function, Script, Data, Theme
from collections import namedtuple
from math import sqrt, exp, sin

Margin = namedtuple("Margin", ("top", "right", "bottom", "left"))

K = 1
omega_0 = 2
e0 = 1

def second_order(t, zeta):
    if t <= 0:
        return 0
    if zeta > 1:
        p1 = -zeta * omega_0 + omega_0 * sqrt(zeta * zeta - 1)
        p2 = -zeta * omega_0 - omega_0 * sqrt(zeta * zeta - 1)
        return (
          K * omega_0 / (2 * sqrt(zeta * zeta - 1)) * (
            exp(p1 * t) - exp(p2 * t)
          )
        )
    else:
        return (
          K * omega_0 / sqrt(1 - zeta * zeta) *
          exp(-zeta * omega_0 * t) *
          sin(omega_0 * sqrt(1 - zeta * zeta) * t)
        )
      
xmax = 10
steps = 1000

xvalues = [(xmax * i / steps) for i in range(steps)]
allzeta = [2, 1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.6, 0.4, 0.2]
values = {"allzeta": allzeta, "allvalues": [
    {"key": zeta, "values": [
        {"x": t, "y": second_order(t, zeta)} for t in xvalues
    ]} for zeta in allzeta
]}

data = Data(values)
# print(data.allzeta)
# print(data.allvalues[0])
# print(data.allvalues[0].values)
# print(data.allvalues[0].values[0])
# max(data.allvalues[len(data.allzeta) - 1].values, key=lambda d: d["y"])["y"]


def make_script(script):
    margin = Margin(10, 30, 30, 60)
    width = 460 - margin.left - margin.right
    height = 300 - margin.top - margin.bottom

    script(
        "svg",
        d3.select(script.plot_id)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", f"translate({margin.left}, {margin.top})"),
    )
    x = script(
        "x",
        d3.scaleLinear()
        .domain(d3.extent(data.allvalues[0].values, function("d").inline("d.x")))
        .range([0, width]),
    )

    script(
        svg.append("g")
        .attr("transform", f"translate(0, {height})")
        .call(d3.axisBottom(x).tickFormat(d3.format(".0f")))
    )
    ymax = max(data.allvalues[len(data.allzeta.data) - 1].values.data, key=lambda d: d["y"])["y"]
    y = script("y", d3.scaleLinear().domain([-ymax, ymax]).range([height, -1]).nice())

    color = script(
        "color",
        d3.scaleLinear()
        .domain([max(values["allzeta"]), min(values["allzeta"])])
        .range(["gold", "deepskyblue"]),
    )

    script(svg.append("g").call(d3.axisLeft(y).tickFormat(d3.format(".1f"))))

    script(
        svg.selectAll(".line")
        .data(data.allvalues)
        .enter()
        .append("path")
        .attr("fill", "none")
        .attr("stroke", js("d => color(d.key)"))
        .attr(
            "d",
            function("d").inline(
                d3.line().x(function("d").inline("x(d.x)")).y(function("d").inline("y(d.y)"))(js("d.values"))
            ),
        )
    )
    return script

theme = Theme.DARK

scripts = {f"Title {i}": make_script(script) for i, script in enumerate(Script.multiple(4))}
# render(values, scripts, grid=2, style=theme.style)
save(values, scripts, "impulse.pdf", grid=2)
