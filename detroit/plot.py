import functools

def wrap_method(cls, method):
    """
    Decorator used to generate a method to the `Plot` class
    automatically given the class and a name of the method
    """
    def wrapper(data, options=None):
        if options is None:
            return js(f"Plot.{method}({data})")
        return js(f"Plot.{method}({data}, {options})")
    return wrapper

def wrap_methods(cls):
    """
    Decorator used to generate all methods to the `Plot` class
    automatically based on `Plot.WRAP_METHODS`
    """
    for name in cls.WRAP_METHODS:
        setattr(cls, name, wrap_method(cls, name))
    return cls


@wrap_methods
class Plot:
    """
    Observable Plot wrapper

    See documentation on 'https://observablehq.com/plot/getting-started'
    """

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

def convert(*obj):
    if isinstance(obj, list):
        pass
    if isinstance(obj, dict):
        pass
    elif isinstance(obj, str):
        pass
    else:
        return str(obj)

class js:
    """
    Useful class to remove quotes when string is represented

    Example

    print([js("(x) => x / 1000")]) # [(x) => x / 1000]
    # instead of ["(x) => x / 1000"]
    """
    def __init__(self, string: str):
        self.string = string
    def __str__(self):
        return self.string
    def __repr__(self):
        return self.string

# print(Plot.plot({"marginLeft": 120, "transform": js("(x) => x / 1000"), "marks": [Plot.ruleX([0]), Plot.tickX("traffic", {"x": "vehicles", "y": "location", "strokeOpacity": 0.3})]}))
