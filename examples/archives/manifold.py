import polars as pl
from sklearn import datasets, manifold

from detroit import Plot, Theme, arrange, js, render, save

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

theme = Theme.DARK

data = {}
plots = {}
for title, method in lle_methods:
    lle = manifold.LocallyLinearEmbedding(method=method, **params)
    points = lle.fit_transform(spoints)
    df = pl.from_numpy(points, schema=["colx", "coly"]).insert_column(
        2, pl.Series("color", scolors)
    )
    data[method] = arrange(df)
    plots[title] = Plot.dot(
        js(f"data.{method}"), {"x": "colx", "y": "coly", "stroke": "color"}
    ).plot({"style": theme.plot})

render(data, plots, grid=2, style=theme.style)  # grid = number of columns
# save(data, plots, "dark-manifold.png", grid=2, style=theme.style)
