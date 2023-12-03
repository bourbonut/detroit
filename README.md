# detroit

detroit is wrapper for Python of [d3js](https://d3js.org/) especially focus on [Observable Plot](https://observablehq.com/plot/) in the current version.

# Installation

```shell
pip install pip install git+https://github.com/bourbonut/detroit.git
```
Then you will need to install a browser through the Python package `playwright`. For the moment, only `chromium` is supported.
```shell
playwright install chromium
```

# Usage

- Render a plot in your browser

```py
import polars as pl
from jinja2 import Environment, PackageLoader, select_autoescape
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from detroit import Plot, js, render, save

mnsit = load_digits()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(mnsit.data)
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)

df = pl.DataFrame(components, schema=["Component 1", "Component 2"]).insert_column(2, pl.Series("digit", mnsit.target))
data = df.to_dicts()
plot = Plot.plot({
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

render(data, plot)
```

- Save your figure as `.svg`, `.png` or `.pdf`

```py
# Replace
render(data, plot)
# By
save(data, plot, "figure.pdf")
save(data, plot, "figure.svg")
save(data, plot, "figure.png", scale_factor=2, width=640, height=440)
```

**Note :** `.svg` does not support the legend. However, `.png` and `.pdf` support it !
