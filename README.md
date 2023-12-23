<p align="center">
    <img style="border-radius:15px" src="https://raw.githubusercontent.com/bourbonut/detroit/main/docs/source/_static/logo.png"></img>
    <br />
    <a href="https://pypi.org/project/detroit/">
        <img src="https://img.shields.io/pypi/v/detroit.svg?style=flat&logo=pypi" alt="PyPI Latest Release">
    </a>
    <a href='https://detroit.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/detroit/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://img.shields.io/badge/license-MIT-red.svg?style=flat">
        <img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" alt="BSD-3-Clause">
    </a>
</p>

detroit is wrapper for Python of [d3js](https://d3js.org/) and [Observable Plot](https://observablehq.com/plot/).

- [Documentation](https://detroit.readthedocs.io/en/latest/)

# Installation

```sh
pip install detroit
```

Then you will need to install a browser through the Python package `playwright`.
For the moment, only `chromium` is supported.

```sh
playwright install chromium
```

# Features

- Write as close as possible `d3` and `Plot` code
- Render one or multiple plots in your browser or in your jupyter notebook
- Customize style as you want
- Save them into `.svg`, `.png` or `.pdf`

# Quick Example


```py
import polars as pl
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from detroit import Plot, js, render, save

mnsit = load_digits()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(mnsit.data)
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)

# Prepare your data with Polars, Pandas or manually
df = pl.DataFrame(components, schema=["Component 1", "Component 2"])
df = df.insert_column(2, pl.Series("digit", mnsit.target))

plot = Plot.plot({
  "style": {"backgroundColor": "#161b22", "color": "#e6edf3"},
  "symbol": {"legend": js("true")},
  "color": {"scheme": "rainbow"},
  "marks": [
      Plot.dot(js("data"), {
          "x": "Component 1",
          "y": "Component 2",
          "stroke": "digit",
          "symbol": "digit"
      })
  ]
})

render(df, plot, style={"body": {"background": "#161b22", "color": "#e6edf3"}})
```

<p align="center">
    <img src="https://raw.githubusercontent.com/bourbonut/detroit/main/docs/source/figures/quick.png"></img>
</p>
