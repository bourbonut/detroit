from __future__ import annotations
from .utils import js
from typing import Iterator

def wrap_method_d3(cls, method):
    """
    Decorator used to generate a method to the :code:`d3` class
    automatically given the class and a name of the method
    """
    def wrapper(*args, no_arg=False):
        if no_arg:
            return js(f"d3.{method}")
        if len(args) and isinstance(args[0], d3):
            arguments = ", ".join(map(repr, args[1:]))
            return d3(f"{args[0]}.{method}({arguments})")
        arguments = ", ".join(map(repr, args))
        return d3(f"d3.{method}({arguments})")
    return wrapper

def wrap_constant_d3(cls, method):
    """
    Decorator used to generate a  to the :code:`d3` class
    automatically given the class and a name of the method
    """
    def wrapper():
        return d3(f"d3.{method}")
    return wrapper

def wrap_methods_constants(cls):
    """
    Decorator used to generate all methods and constants
    to the :code:`d3` class automatically based on :code:`d3.WRAP_METHODS`
    and :code:`d3.WRAP_CONSTANTS`
    """
    for name in cls.WRAP_METHODS:
        setattr(cls, name, wrap_method_d3(cls, name))
    for name in cls.WRAP_CONSTANTS:
        setattr(cls, name, wrap_constant_d3(cls, name))
    return cls

@wrap_methods_constants
class d3:
    """
    Class used to mimick javascript syntax for :code:`d3`

    See `documentation <https://d3js.org/getting-started>`_.

    Examples
    --------

    >>> from detroit import d3, js
    >>> d3.axisBottom(js("x")).tickFormat(d3.format(".0f"))
    d3.axisBottom(x).tickFormat(d3.format('.0f'))
    """
    WRAP_METHODS = [
        "Adder",
        "Delaunay",
        "FormatSpecifier",
        "InternMap",
        "InternSet",
        "Node",
        "Path",
        "Voronoi",
        "ZoomTransform",
        "active",
        "append",
        "arc",
        "area",
        "areaRadial",
        "ascending",
        "attr",
        "autoType",
        "axisBottom",
        "axisLeft",
        "axisRight",
        "axisTop",
        "bin",
        "bisect",
        "bisectCenter",
        "bisectLeft",
        "bisectRight",
        "bisector",
        "blob",
        "blur",
        "blur2",
        "blurImage",
        "brush",
        "brushSelection",
        "brushX",
        "brushY",
        "buffer",
        "chord",
        "chordDirected",
        "chordTranspose",
        "cluster",
        "color",
        "contourDensity",
        "contours",
        "count",
        "create",
        "creator",
        "cross",
        "csv",
        "csvFormat",
        "csvFormatBody",
        "csvFormatRow",
        "csvFormatRows",
        "csvFormatValue",
        "csvParse",
        "csvParseRows",
        "cubehelix",
        "cumsum",
        "curveBasis",
        "curveBasisClosed",
        "curveBasisOpen",
        "curveBumpX",
        "curveBumpY",
        "curveBundle",
        "curveCardinal",
        "curveCardinalClosed",
        "curveCardinalOpen",
        "curveCatmullRom",
        "curveCatmullRomClosed",
        "curveCatmullRomOpen",
        "curveLinear",
        "curveLinearClosed",
        "curveMonotoneX",
        "curveMonotoneY",
        "curveNatural",
        "curveStep",
        "curveStepAfter",
        "curveStepBefore",
        "descending",
        "deviation",
        "difference",
        "disjoint",
        "dispatch",
        "domain",
        "drag",
        "dragDisable",
        "dragEnable",
        "dsv",
        "dsvFormat",
        "easeBack",
        "easeBackIn",
        "easeBackInOut",
        "easeBackOut",
        "easeBounce",
        "easeBounceIn",
        "easeBounceInOut",
        "easeBounceOut",
        "easeCircle",
        "easeCircleIn",
        "easeCircleInOut",
        "easeCircleOut",
        "easeCubic",
        "easeCubicIn",
        "easeCubicInOut",
        "easeCubicOut",
        "easeElastic",
        "easeElasticIn",
        "easeElasticInOut",
        "easeElasticOut",
        "easeExp",
        "easeExpIn",
        "easeExpInOut",
        "easeExpOut",
        "easeLinear",
        "easePoly",
        "easePolyIn",
        "easePolyInOut",
        "easePolyOut",
        "easeQuad",
        "easeQuadIn",
        "easeQuadInOut",
        "easeQuadOut",
        "easeSin",
        "easeSinIn",
        "easeSinInOut",
        "easeSinOut",
        "enter",
        "every",
        "extent",
        "fcumsum",
        "filter",
        "flatGroup",
        "flatRollup",
        "forceCenter",
        "forceCollide",
        "forceLink",
        "forceManyBody",
        "forceRadial",
        "forceSimulation",
        "forceX",
        "forceY",
        "format",
        "formatDefaultLocale",
        "formatLocale",
        "formatPrefix",
        "formatSpecifier",
        "fsum",
        "geoAlbers",
        "geoAlbersUsa",
        "geoArea",
        "geoAzimuthalEqualArea",
        "geoAzimuthalEqualAreaRaw",
        "geoAzimuthalEquidistant",
        "geoAzimuthalEquidistantRaw",
        "geoBounds",
        "geoCentroid",
        "geoCircle",
        "geoClipAntimeridian",
        "geoClipCircle",
        "geoClipExtent",
        "geoClipRectangle",
        "geoConicConformal",
        "geoConicConformalRaw",
        "geoConicEqualArea",
        "geoConicEqualAreaRaw",
        "geoConicEquidistant",
        "geoConicEquidistantRaw",
        "geoContains",
        "geoDistance",
        "geoEqualEarth",
        "geoEqualEarthRaw",
        "geoEquirectangular",
        "geoEquirectangularRaw",
        "geoGnomonic",
        "geoGnomonicRaw",
        "geoGraticule",
        "geoGraticule10",
        "geoIdentity",
        "geoInterpolate",
        "geoLength",
        "geoMercator",
        "geoMercatorRaw",
        "geoNaturalEarth1",
        "geoNaturalEarth1Raw",
        "geoOrthographic",
        "geoOrthographicRaw",
        "geoPath",
        "geoProjection",
        "geoProjectionMutator",
        "geoRotation",
        "geoStereographic",
        "geoStereographicRaw",
        "geoStream",
        "geoTransform",
        "geoTransverseMercator",
        "geoTransverseMercatorRaw",
        "gray",
        "greatest",
        "greatestIndex",
        "group",
        "groupSort",
        "groups",
        "hcl",
        "hierarchy",
        "histogram",
        "hsl",
        "html",
        "image",
        "index",
        "indexes",
        "interpolate",
        "interpolateArray",
        "interpolateBasis",
        "interpolateBasisClosed",
        "interpolateBlues",
        "interpolateBrBG",
        "interpolateBuGn",
        "interpolateBuPu",
        "interpolateCividis",
        "interpolateCool",
        "interpolateCubehelix",
        "interpolateCubehelixDefault",
        "interpolateCubehelixLong",
        "interpolateDate",
        "interpolateDiscrete",
        "interpolateGnBu",
        "interpolateGreens",
        "interpolateGreys",
        "interpolateHcl",
        "interpolateHclLong",
        "interpolateHsl",
        "interpolateHslLong",
        "interpolateHue",
        "interpolateInferno",
        "interpolateLab",
        "interpolateMagma",
        "interpolateNumber",
        "interpolateNumberArray",
        "interpolateObject",
        "interpolateOrRd",
        "interpolateOranges",
        "interpolatePRGn",
        "interpolatePiYG",
        "interpolatePlasma",
        "interpolatePuBu",
        "interpolatePuBuGn",
        "interpolatePuOr",
        "interpolatePuRd",
        "interpolatePurples",
        "interpolateRainbow",
        "interpolateRdBu",
        "interpolateRdGy",
        "interpolateRdPu",
        "interpolateRdYlBu",
        "interpolateRdYlGn",
        "interpolateReds",
        "interpolateRgb",
        "interpolateRgbBasis",
        "interpolateRgbBasisClosed",
        "interpolateRound",
        "interpolateSinebow",
        "interpolateSpectral",
        "interpolateString",
        "interpolateTransformCss",
        "interpolateTransformSvg",
        "interpolateTurbo",
        "interpolateViridis",
        "interpolateWarm",
        "interpolateYlGn",
        "interpolateYlGnBu",
        "interpolateYlOrBr",
        "interpolateYlOrRd",
        "interpolateZoom",
        "interrupt",
        "intersection",
        "interval",
        "isoFormat",
        "isoParse",
        "json",
        "lab",
        "lch",
        "least",
        "leastIndex",
        "line",
        "lineRadial",
        "link",
        "linkHorizontal",
        "linkRadial",
        "linkVertical",
        "local",
        "map",
        "matcher",
        "max",
        "maxIndex",
        "mean",
        "median",
        "medianIndex",
        "merge",
        "min",
        "minIndex",
        "mode",
        "namespace",
        "nice",
        "now",
        "on",
        "pack",
        "packEnclose",
        "packSiblings",
        "pairs",
        "partition",
        "path",
        "pathRound",
        "permute",
        "pie",
        "piecewise",
        "pointRadial",
        "pointer",
        "pointers",
        "polygonArea",
        "polygonCentroid",
        "polygonContains",
        "polygonHull",
        "polygonLength",
        "precisionFixed",
        "precisionPrefix",
        "precisionRound",
        "projection",
        "property",
        "quadtree",
        "quantile",
        "quantileIndex",
        "quantileSorted",
        "quantize",
        "quickselect",
        "radialArea",
        "radialLine",
        "randomBates",
        "randomBernoulli",
        "randomBeta",
        "randomBinomial",
        "randomCauchy",
        "randomExponential",
        "randomGamma",
        "randomGeometric",
        "randomInt",
        "randomIrwinHall",
        "randomLcg",
        "randomLogNormal",
        "randomLogistic",
        "randomNormal",
        "randomPareto",
        "randomPoisson",
        "randomUniform",
        "randomWeibull",
        "range",
        "rank",
        "reduce",
        "reverse",
        "rgb",
        "ribbon",
        "ribbonArrow",
        "rollup",
        "rollups",
        "scale",
        "scaleBand",
        "scaleDiverging",
        "scaleDivergingLog",
        "scaleDivergingPow",
        "scaleDivergingSqrt",
        "scaleDivergingSymlog",
        "scaleIdentity",
        "scaleLinear",
        "scaleLog",
        "scaleOrdinal",
        "scalePoint",
        "scalePow",
        "scaleQuantile",
        "scaleQuantize",
        "scaleRadial",
        "scaleSequential",
        "scaleSequentialLog",
        "scaleSequentialPow",
        "scaleSequentialQuantile",
        "scaleSequentialSqrt",
        "scaleSequentialSymlog",
        "scaleSqrt",
        "scaleSymlog",
        "scaleThreshold",
        "scaleTime",
        "scaleUtc",
        "scan",
        "select",
        "selectAll",
        "selection",
        "selector",
        "selectorAll",
        "shuffle",
        "shuffler",
        "size",
        "some",
        "sort",
        "stack",
        "stackOffsetDiverging",
        "stackOffsetExpand",
        "stackOffsetNone",
        "stackOffsetSilhouette",
        "stackOffsetWiggle",
        "stackOrderAppearance",
        "stackOrderAscending",
        "stackOrderDescending",
        "stackOrderInsideOut",
        "stackOrderNone",
        "stackOrderReverse",
        "stratify",
        "style",
        "subset",
        "sum",
        "superset",
        "svg",
        "symbol",
        "text",
        "thresholdFreedmanDiaconis",
        "thresholdScott",
        "thresholdSturges",
        "tickFormat",
        "tickIncrement",
        "tickStep",
        "ticks",
        "timeDay",
        "timeDays",
        "timeFormat",
        "timeFormatDefaultLocale",
        "timeFormatLocale",
        "timeFriday",
        "timeFridays",
        "timeHour",
        "timeHours",
        "timeInterval",
        "timeMillisecond",
        "timeMilliseconds",
        "timeMinute",
        "timeMinutes",
        "timeMonday",
        "timeMondays",
        "timeMonth",
        "timeMonths",
        "timeParse",
        "timeSaturday",
        "timeSaturdays",
        "timeSecond",
        "timeSeconds",
        "timeSunday",
        "timeSundays",
        "timeThursday",
        "timeThursdays",
        "timeTickInterval",
        "timeTicks",
        "timeTuesday",
        "timeTuesdays",
        "timeWednesday",
        "timeWednesdays",
        "timeWeek",
        "timeWeeks",
        "timeYear",
        "timeYears",
        "timeout",
        "timer",
        "timerFlush",
        "transition",
        "transpose",
        "tree",
        "treemap",
        "treemapBinary",
        "treemapDice",
        "treemapResquarify",
        "treemapSlice",
        "treemapSliceDice",
        "treemapSquarify",
        "tsv",
        "tsvFormat",
        "tsvFormatBody",
        "tsvFormatRow",
        "tsvFormatRows",
        "tsvFormatValue",
        "tsvParse",
        "tsvParseRows",
        "union",
        "unixDay",
        "unixDays",
        "utcDay",
        "utcDays",
        "utcFormat",
        "utcFriday",
        "utcFridays",
        "utcHour",
        "utcHours",
        "utcMillisecond",
        "utcMilliseconds",
        "utcMinute",
        "utcMinutes",
        "utcMonday",
        "utcMondays",
        "utcMonth",
        "utcMonths",
        "utcParse",
        "utcSaturday",
        "utcSaturdays",
        "utcSecond",
        "utcSeconds",
        "utcSunday",
        "utcSundays",
        "utcThursday",
        "utcThursdays",
        "utcTickInterval",
        "utcTicks",
        "utcTuesday",
        "utcTuesdays",
        "utcWednesday",
        "utcWednesdays",
        "utcWeek",
        "utcWeeks",
        "utcYear",
        "utcYears",
        "variance",
        "window",
        "x",
        "xml",
        "y",
        "zip",
        "zoom",
        "zoomTransform"
    ]

    WRAP_CONSTANTS = [
        "default",
        "namespaces",
        "scaleImplicit",
        "schemeAccent",
        "schemeBlues",
        "schemeBrBG",
        "schemeBuGn",
        "schemeBuPu",
        "schemeCategory10",
        "schemeDark2",
        "schemeGnBu",
        "schemeGreens",
        "schemeGreys",
        "schemeOrRd",
        "schemeOranges",
        "schemePRGn",
        "schemePaired",
        "schemePastel1",
        "schemePastel2",
        "schemePiYG",
        "schemePuBu",
        "schemePuBuGn",
        "schemePuOr",
        "schemePuRd",
        "schemePurples",
        "schemeRdBu",
        "schemeRdGy",
        "schemeRdPu",
        "schemeRdYlBu",
        "schemeRdYlGn",
        "schemeReds",
        "schemeSet1",
        "schemeSet2",
        "schemeSet3",
        "schemeSpectral",
        "schemeTableau10",
        "schemeYlGn",
        "schemeYlGnBu",
        "schemeYlOrBr",
        "schemeYlOrRd",
        "symbolAsterisk",
        "symbolCircle",
        "symbolCross",
        "symbolDiamond",
        "symbolDiamond2",
        "symbolPlus",
        "symbolSquare",
        "symbolSquare2",
        "symbolStar",
        "symbolTimes",
        "symbolTriangle",
        "symbolTriangle2",
        "symbolWye",
        "symbolX",
        "symbols",
        "symbolsFill",
        "symbolsStroke",
        "zoomIdentity"
    ]

    def __init__(self, content="d3"):
        self.content = content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

def wrap_method_svg(cls, method):
    """
    Decorator used to generate a method to the :code:`svg` class
    automatically given the class and a name of the method
    """
    def wrapper(*args, no_arg=False):
        if no_arg:
            return svg(f"svg.{method}")
        if len(args) and isinstance(args[0], svg):
            arguments = ", ".join(map(repr, args[1:]))
            return svg(f"{args[0]}.{method}({arguments})")
        arguments = ", ".join(map(repr, args))
        return svg(f"svg.{method}({arguments})")
    return wrapper

def wrap_methods(cls):
    """
    Decorator used to generate all methods to the :code:`svg` class
    automatically based on :code:`svg.WRAP_METHODS`
    """
    for name in cls.WRAP_METHODS:
        setattr(cls, name, wrap_method_svg(cls, name))
    return cls

@wrap_methods
class svg:
    """
    Class used to mimick javascript syntax for :code:`svg`
    that most of the time is presented in online examples

    Examples
    --------

    >>> from detroit import svg, js, d3
    >>> svg.append("g").call(d3.axisLeft(js("y")).tickFormat(d3.format(".1f")))
    svg.append('g').call(d3.axisLeft(y).tickFormat(d3.format('.1f')))

    """

    WRAP_METHODS = [
        "append",
        "attr",
        "call",
        "data",
        "datum",
        "enter",
        "join",
        "text",
        "select",
        "selectAll",
        "style",
    ]

    def __init__(self, content="svg"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

class Script:
    """
    Class which stores javascript lines of code useful to render
    or save a visualization with :code:`d3` syntax

    Examples
    --------

    >>> from detroit import Script, svg, d3
    >>> script = Script()
    >>> script("svg", d3.select(script.plot_id))
    svg
    >>> script(svg.append("g"))
    >>> print(script)
    var svg = d3.select('#myplot')
    svg.append('g')
    """

    def __init__(self):
        self.code = []
        self.id = "myplot"

    def __call__(self, *args):
        if len(args) > 2:
            raise ValueError("Too many arguments (len(args) > 2)")
        elif len(args) == 2:
            self.code.append(str(js(f"var {args[0]} = {args[1]}")))
            return var(args[0])
        elif len(args) == 1:
            self.code.append(str(js(f"{args[0]}")))
        else:
            raise ValueError("No argument supplied")

    @property
    def plot_id(self):
        """
        Return the id formatted for selection
        """
        return f"#{self.id}"

    @staticmethod
    def multiple(nb: int) -> Iterator[Script]:
        """
        Generate multiple :code:`Script`

        Parameters
        ----------
        nb : int
            number of script

        Returns
        -------
        Iterator[Script]
            multiple :code:`Script`   
        """
        for i in range(nb):
            script = Script()
            script.id = f"plot-{i}"
            yield script

    def __str__(self):
        return "\n".join(map(str, self.code))

class var:
    """
    Class only used to avoid writing :code:`js("var_name")`

    Examples
    --------

    >>> from detroit.d3 import var
    >>> true = var("true")
    >>> [true]
    [true]
    >>> ["true"]
    ["true"]
    """

    def __init__(self, name):
        self.name = name

    def __neg__(self):
        return js(f"-{self.name}")

    def __str__(self):
        return str(js(f"{self.name}"))

    def __repr__(self):
        return str(js(f"{self.name}"))

class function:
    """
    Useful class to simplify inline functions

    Examples
    --------

    >>> from detroit import function
    >>> function("d")("x(d.x)")
    function(d){ return x(d.x); }
    """
    def __init__(self, *args):
        self.args = args

    def __call__(self, arg):
        arguments = ", ".join(self.args)
        return js(f"function({arguments})"+ "{ return " + arg + "; }")
