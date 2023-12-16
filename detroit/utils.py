from markupsafe import Markup

FETCH = Markup("var data;fetch(\"/data\").then(response => response.json()).then(d => {data = d;})")

async def load_svg_functions(env):
    template = env.get_template("svg.html")
    return await template.render_async()


def arrange(obj):
    try:
        import polars as pl
        if isinstance(obj, pl.DataFrame):
            return obj.to_dicts()
    except:
        pass
    try:
        import pandas as pd
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
    except:
        pass
    if isinstance(obj, list):
        if len(obj) == 1:
            obj = obj[0]
            if isinstance(obj, list):
                return [{"x": i, "y": item} for i, item in enumerate(obj)]
        elif len(obj) == 2:
            x, y = obj
            if isinstance(x, list) and isinstance(y, list):
                assert len(x) == len(y), "All inputs must have the same length."
                return [{"x": xi, "y": yi} for xi, yi in zip(x, y)]
            else:
                raise ValueError(f"Only list type supported.")
        elif len(obj) == 3:
            x, y, z = obj
            if all(map(lambda e: isinstance(e, list), (x, y, z))):
                assert len(x) == len(y) == len(z), "All inputs must have the same length."
                return [{"x": xi, "y": yi, "z": zi} for xi, yi, zi in zip(x, y, z)]
            else:
                raise ValueError(f"Only list type supported.")
    return obj
