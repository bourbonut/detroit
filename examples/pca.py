# pip install scikit-learn
import detroit as d3
import polars as pl
from itertools import cycle
from collections import namedtuple
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Prepare data
mnsit = load_digits()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(mnsit.data)
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)

df = pl.DataFrame(components, schema=["Component 1", "Component 2"])
df = df.insert_column(2, pl.Series("digit", mnsit.target))

# Specify the chart's dimensions
width = 928
height = 600

Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])
margin = Margin(50, 30, 30, 40)


# Create the horizontal x scale
x = (
    d3.scale_linear()
    .set_domain([df["Component 1"].min(), df["Component 1"].max()])
    .nice()
    .set_range([margin.left, width - margin.right])
)

# Create the vertical y scale
y = (
    d3.scale_linear()
    .set_domain([df["Component 2"].min(), df["Component 2"].max()])
    .nice()
    .set_range([height - margin.bottom, margin.top])
)

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)

# Append the axis

(
    svg.append("g")
    .attr("transform", f"translate(0, {height - margin.bottom})")
    .call(d3.axis_bottom(x))
    .call(lambda g: g.select(".domain").remove())
    .call(
        lambda g: g.append("text")
        .attr("x", width - margin.right)
        .attr("y", -4)
        .attr("fill", "#000")
        .attr("font-weight", "bold")
        .attr("text-anchor", "end")
        .text("Component 1")
    )
)

(
    svg.append("g")
    .attr("transform", f"translate({margin.left}, 0)")
    .call(d3.axis_left(y))
    .call(lambda g: g.select(".domain").remove())
    .call(
        lambda g: g.select(".tick:last-of-type")
        .select("text")
        .clone()
        .attr("x", 4)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text("Component 2")
    )
)

# Append the symbols

symbol_type = d3.scale_ordinal(df["digit"].unique().sort().to_list(), d3.SYMBOLS_STROKE)

color = d3.scale_sequential(
    [df["digit"].min(), df["digit"].max()], d3.interpolate_rainbow
)

(
    svg.append("g")
    .attr("fill", "none")
    .attr("stroke-width", 1.5)
    .select_all("circle")
    .data(df.iter_rows())
    .join("g")
    .attr("transform", lambda d: f"translate({x(d[0])}, {y(d[1])})")
    .append("path")
    .attr("d", lambda d: d3.symbol(symbol_type(d[2]))())
    .attr("stroke", lambda d: color(d[2]))
)

# Legend

labels = df["digit"].unique().sort()
nb_columns = labels.len()  # number of labels
offset = 40  # Space between legend labels
symbol_size = 3

legend = svg.select_all("legend").data(labels.to_list()).enter().append("g")

(
    legend.append("g")
    .attr("transform", lambda _, i: f"translate({i * offset + margin.left - symbol_size * 4}, {30 - symbol_size * 1.5})")
    .append("path")
    .attr("d", lambda d: d3.symbol(symbol_type(d))())
    .style("stroke-width", 1.5)
    .style("stroke", lambda d: color(d))
    .style("fill", "none")
)

(
    legend.append("text")
    .attr("x", lambda _, i: i * offset + margin.left)
    .attr("y", 30)
    .text(lambda d: str(d))
    .style("fill", "black") # change "black" to "white" for white text
    .style("font-size", 15)
)

# For white axis and text
# svg.select_all("path.domain").attr("stroke", "white")
# svg.select_all("g.tick").select_all("line").attr("stroke", "white")
# svg.select_all("g.tick").select_all("text").attr("fill", "white").attr("stroke", "none")
# svg.select_all("text").attr("fill", "white").attr("stroke", "none")

with open("pca.svg", "w") as file:
    file.write(str(svg))
