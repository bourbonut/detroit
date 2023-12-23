def wrap_method(cls, method):
    """
    Decorator used to generate a method to the `Plot` class
    automatically given the class and a name of the method
    """
    def wrapper(*args, no_arg=False):
        if no_arg:
            return js(f"Plot.{method}")
        if len(args) and isinstance(args[0], Plot):
            arguments = ", ".join(map(repr, args[1:]))
            return Plot(f"{args[0]}.{method}({arguments})")
        arguments = ", ".join(map(repr, args))
        return Plot(f"Plot.{method}({arguments})")
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
    Class which mimick :code:`Plot`

    See `documentation <https://observablehq.com/plot/getting-started>`_.

    Examples
    --------

    >>> from detroit import Plot, js
    >>> Plot.dot(js("data"), {
    ...     "x": "Component 1",
    ...     "y": "Component 2",
    ...     "stroke": "digit",
    ...     "symbol": "digit",
    ... }).plot({
    ...     "symbol": {"legend": js("true")},
    ...     "color": {"scheme": "rainbow"},
    ... })
    Plot.dot(data, {'x': 'Component 1', 'y': 'Component 2', 'stroke': 'digit', 'symbol': 'digit'}).plot({'symbol': {'legend': true}, 'color': {'scheme': 'rainbow'}})
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

    def __init__(self, content="Plot"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
