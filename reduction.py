import asyncio

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
# save(data, plot, "figure.pdf")
