import functools

def wrap_method(cls, method):
    def wrapper(data, options=None):
        if options is None:
            return js(f"Plot.{method}({data})")
        return js(f"Plot.{method}({data}, {options})")
    return wrapper

def wrap_methods(cls):
    for name in cls.WRAP_METHODS:
        setattr(cls, name, wrap_method(cls, name))
    return cls


@wrap_methods
class Plot:

    WRAP_METHODS = [
      "area",
      "areaX",
      "areaY",
      "arrow",
      "auto",
      "autoSpec",
      "axisFx",
      "axisFy",
      "axisX",
      "axisY",
      "barX",
      "barY",
      "bin",
      "binX",
      "binY",
      "bollinger",
      "bollingerX",
      "bollingerY",
      "boxX",
      "boxY",
      "cell",
      "cellX",
      "cellY",
      "centroid",
      "circle",
      "cluster",
      "column",
      "contour",
      "crosshair",
      "crosshairX",
      "crosshairY",
      "delaunayLink",
      "delaunayMesh",
      "density",
      "dodgeX",
      "dodgeY",
      "dot",
      "dotX",
      "dotY",
      "filter",
      "formatIsoDate",
      "formatMonth",
      "formatWeekday",
      "frame",
      "geo",
      "geoCentroid",
      "graticule",
      "gridFx",
      "gridFy",
      "gridX",
      "gridY",
      "group",
      "groupX",
      "groupY",
      "groupZ",
      "hexagon",
      "hexbin",
      "hexgrid",
      "hull",
      "identity",
      "image",
      "indexOf",
      "initializer",
      "interpolateNearest",
      "interpolateNone",
      "interpolatorBarycentric",
      "interpolatorRandomWalk",
      "legend",
      "line",
      "lineX",
      "lineY",
      "linearRegressionX",
      "linearRegressionY",
      "link",
      "map",
      "mapX",
      "mapY",
      "marks",
      "normalize",
      "normalizeX",
      "normalizeY",
      "plot",
      "pointer",
      "pointerX",
      "pointerY",
      "raster",
      "rect",
      "rectX",
      "rectY",
      "reverse",
      "ruleX",
      "ruleY",
      "scale",
      "select",
      "selectFirst",
      "selectLast",
      "selectMaxX",
      "selectMaxY",
      "selectMinX",
      "selectMinY",
      "shuffle",
      "sort",
      "sphere",
      "spike",
      "stackX",
      "stackX1",
      "stackX2",
      "stackY",
      "stackY1",
      "stackY2",
      "text",
      "textX",
      "textY",
      "tickX",
      "tickY",
      "tip",
      "transform",
      "tree",
      "treeLink",
      "treeNode",
      "valueof",
      "vector",
      "vectorX",
      "vectorY",
      "version",
      "voronoi",
      "voronoiMesh",
      "window",
      "windowX",
      "windowY",
    ]

def convert(obj):
    if isinstance(obj, list):
        pass
    if isinstance(obj, dict):
        pass
    elif isinstance(obj, str):
        pass
    else:
        return str(obj)

def tojson(*args):
    are_iterable = all(isinstance(obj, Iterable) for obj in args)
    if len(args) == 2 and are_iterable:
        x, y = args
        x = list(x)
        y = list(y)
        assert len(x) == len(y), "x and y must have same size."
        data = [{"key": 0, "values": [{"x": a, "y": b} for a, b in zip(x, y)]}]
    elif len(args) == 2 and are_iterable:
        x, y, keys = args
        x = list(x)
        y = list(y)
        assert len(keys) == len(y), "keys and y must have same size."
        if isinstance(x[0], Iterable):
            x = list(map(list, x))
        else:
            x = [x for _ in range(len(y))]
        y = list(map(list, y))
        assert all(len(xi) == len(yi) for xi, yi in zip(x, y))
        data = [
            {"key": key, "values": [{"x": a, "y": b} for a, b in zip(xi, yi)]}
            for key, xi, yi in zip(keys, x, y)
        ]
    return data

class js:
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string
    def __repr__(self):
        return self.string

print(Plot.plot({"marginLeft": 120, "transform": js("(x) => x / 1000"), "marks": [Plot.ruleX([0]), Plot.tickX("traffic", {"x": "vehicles", "y": "location", "strokeOpacity": 0.3})]}))
