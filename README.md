# detroit

detroit is wrapper for Python of [d3js](https://d3js.org/) especially focus on [Observable Plot](https://observablehq.com/plot/) in the current version.

## Installation

```shell
pip install git+https://github.com/bourbonut/detroit.git
```
Then you will need to install a browser through the Python package `playwright`. For the moment, only `chromium` is supported.
```shell
playwright install chromium
```

## Features

- Render in your browser a plot
- Render in your browser multiple plots
- Save your plot to `.png`, `.svg` or `.pdf`
- Support `pandas` and `polars` dataframes
- Support `jupyter` notebook

## Usage

- Render a plot in `jupyter` notebook

![jupyter example](docs/jupyter.png)

- Render a plot in your browser

```py
import polars as pl
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from detroit import Plot, js, render, save, style, Theme

mnsit = load_digits()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(mnsit.data)
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)

# Prepare your data with Polars, Pandas or manually
df = pl.DataFrame(components, schema=["Component 1", "Component 2"])
df = df.insert_column(2, pl.Series("digit", mnsit.target))

# You can choose a theme or keep default colors
theme = style(Theme.DARK) # or Theme.JUPYTER_DARK, Theme.JUPYTER_DARK_CENTER

plot = Plot.plot({
    "style": theme.plot,              # change colors of plot div precisely
    "symbol": {"legend": js("true")},
    "marks": [
        Plot.dot(js("data"), {
            "x": "Component 1",
            "y": "Component 2",
            "stroke": "digit",
            "symbol": "digit"
        })
    ]
})

render(df, plot, style=theme.body) # change background color and text color
```

Then type in your browser `localhost:5000` to view your plot.

**Note :** You can also write your own style if you want :
```py
plot = Plot.plot({
    "style": {"backgroundColor": "#111111", "color": "white"}, # check Observable Plot documentation
    "symbol": {"legend": js("true")},
    "marks": [
        Plot.dot(js("data"), {
            "x": "Component 1",
            "y": "Component 2",
            "stroke": "digit",
            "symbol": "digit"
        })
    ]
})

style = """
body {
    background: #111111;
    color: white;
    display: flex;
    justify-content: center;
}
"""
render(df, plot, style=style)
# Or save it in a file and load it
render(df, plot, style="style.css")
```

- Save your figure as `.svg`, `.png` or `.pdf`

```py
# Replace
render(df, plot)
# By
save(df, plot, "figure.pdf")
save(df, plot, "figure.svg")
save(df, plot, "figure.png", scale_factor=2) # scale factor helps to improve the quality of the image
```

- Multiple plots

```py
import polars as pl
from sklearn import datasets, manifold
from detroit import Plot, js, render, save
from detroit.utils import arrange

nsamples = 1500
spoints, scolors = datasets.make_s_curve(nsamples, random_state=0)

params = {
    "n_neighbors": 12,
    "n_components": 2,
    "eigen_solver": "auto",
    "random_state": 0,
}
lle_methods = [
    ("Standard locally linear embedding", "standard"),
    ("Local tangent space alignment", "ltsa"),
    ("Hessian eigenmap", "hessian"),
    ("Modified locally linear embedding", "modified"),
]

data = {}
plot = {}
for title, method in lle_methods:
    lle = manifold.LocallyLinearEmbedding(method=method, **params)
    points = lle.fit_transform(spoints)
    df = pl.from_numpy(points, schema=["colx", "coly"]).insert_column(2, pl.Series("color", scolors))
    data[method] = arrange(df)
    plot[title] = Plot.plot({
        "marks": [Plot.dot(js(f"data.{method}"), {"x": "colx", "y": "coly", "stroke": "color"})]
    })

render(data, plot, grid=2) # grid = number of columns, by default, there is only one column
# save(data, plot, "manifold.svg", grid=2)
```
