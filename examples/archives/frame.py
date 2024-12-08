import polars as pl  # or import pandas as pd

from detroit import (  # useful classes to simplify js syntax
    Data,
    Plot,
    arrange,  # simplify a DataFrame into an explotable dictionary
    js,
    render,  # render the script in your browser
    save,
)

# https://observablehq.com/@observablehq/plot-barley-trellis
# Load data
df = pl.read_csv("barley.csv")
barley = Data.arrange(df)

true = js("true")

plot = Plot.plot(
    {
        "height": 800,
        "marginRight": 90,
        "marginLeft": 110,
        "grid": true,
        "x": {"nice": true},
        "y": {"inset": 5},
        "color": {"type": "categorical"},
        "marks": [
            Plot.frame(),
            Plot.dot(
                barley,
                {
                    "x": "yield",
                    "y": "variety",
                    "fy": "site",
                    "stroke": "year",
                    "sort": {"y": "x", "fy": "x", "reduce": "median", "reverse": true},
                },
            ),
        ],
    }
)

save(df, plot, "light-barley.svg")
