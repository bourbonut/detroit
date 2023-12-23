import asyncio
from enum import Enum, auto
from pathlib import Path
from typing import Union, Dict, List

from jinja2 import ChoiceLoader, Environment, PackageLoader, select_autoescape
from markupsafe import Markup
from playwright.async_api import async_playwright
from quart import Quart, request

from .d3 import Script
from .plot import Plot
from .style import CSS, GRID
from .utils import Data, DataInput, arrange

try:
    import nest_asyncio
    nest_asyncio.apply()
    from IPython import get_ipython
    from IPython.display import HTML, display
    JUPYTER_INSTALLED = True
except:
    JUPYTER_INSTALLED = False

FETCH = Markup("var data;fetch(\"/data\").then(response => response.json()).then(d => {data = d;})")

JSCode = Union[Plot, Script]
JSInput = Union[Dict[str, JSCode], List[JSCode]]

class PlotType:
    SINGLE_PLOT = auto()
    MULTIPLE_PLOTS = auto()
    SINGLE_D3 = auto()
    MULTIPLE_D3 = auto()
    UNIDENTIFIED = auto()

def jupyter_environment():
    """
    Check if the code is executed in a jupyter environment
    """
    try:
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except NameError:
        return False

def identify(plot: JSInput) -> PlotType:
    """
    Identify the type of the plot argument

    Parameters
    ----------
    plot : JSInput
        plot javascript code

    Returns
    -------
    PlotType
        type of the plot
    """
    if isinstance(plot, Plot):
        return PlotType.SINGLE_PLOT
    elif isinstance(plot, Script):
        return PlotType.SINGLE_D3
    elif isinstance(plot, dict):
        objs = plot.values()
        if all(map(lambda obj: isinstance(obj, Plot), objs)):
            return PlotType.MULTIPLE_PLOTS
        elif all(map(lambda obj: isinstance(obj, Script), objs)):
            return PlotType.MULTIPLE_D3
    elif isinstance(plot, list):
        if all(map(lambda obj: isinstance(obj, Plot), plot)):
            return PlotType.MULTIPLE_PLOTS
        elif all(map(lambda obj: isinstance(obj, Script), plot)):
            return PlotType.MULTIPLE_D3
    return PlotType.UNIDENTIFIED

async def html(data: dict, plot: JSInput, style:Union[str, dict]=None, fetch:bool=True, svg:bool=False, grid:int=1) -> str:
    """
    Return HTML content filled by arguments

    Parameters
    ----------
    data : DataInput
        data used for plots
    plot : JSInput
        plot javascript code
    style : Union[str, dict]
        a file or a dictionary defining a CSS file
    fetch : bool
        True if data is fetched by the javascript code else the data is directly written into javascript
    svg : bool
        True to get javascript functions to generate a svg object in javascript
    grid : int
        number of columns

    Returns
    -------
    str
        HTML content filled by arguments
    """
    loader = ChoiceLoader([PackageLoader("detroit", "templates"), PackageLoader("detroit", "static")])
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    plot_type = identify(plot)
    style = CSS(style)

    if plot_type == PlotType.UNIDENTIFIED:
        raise TypeError("Unsupported type of argument \"plot\"")
    elif plot_type == PlotType.MULTIPLE_D3 or plot_type == PlotType.MULTIPLE_PLOTS:
        single = False
        style.update(GRID(grid))
        if isinstance(plot, dict):
            code = {
                id: {"title": title, "code": Markup(code)}
                for id, (title, code) in enumerate(plot.items())
            }
        else:
            code = {
                id: {"title": "", "code": Markup(code)}
                for id, code in enumerate(plot)
            }
        id = f"plot-{len(plot) - 1}"
        width_code = "boundingRect.width" if grid > 1 else "svg.getBoundingClientRect().width"
        serialize_code = f"mysvg = serialize(makeSVGfromGrid(div, svg, {grid}));" if svg else ""
    else:
        single = True
        code = Markup(plot)
        id = "myplot"
        width_code = "svg.getBoundingClientRect().width"
        serialize_code=(
            "mysvg = serialize(svg);"
            if plot_type == PlotType.SINGLE_D3
            else "mysvg = serialize(makeSVGfromSimple(div, svg));"
        )

    data = Markup(f"const data = {data};")
    if plot_type == PlotType.SINGLE_D3 or plot_type == PlotType.MULTIPLE_D3:
        template = env.get_template("d3.html")
    else:
        template = env.get_template("plot.html")
    return await template.render_async(
        single = single,
        code=code,
        data=data,
        style=str(style),
        serialize=svg,
        serialize_code=serialize_code,
        width_code=width_code,
        id=id,
    )

async def _save(data: dict, plot: JSInput, output: Union[Path, str], style: Union[str, dict], grid: int, scale_factor: float):
    """
    Save the plot into a `output` file given arguments.
    It supports :

    * :code:`.svg` files
    * :code:`.png` files
    * :code:`.pdf` files

    Parameters
    ----------
    data : DataInput
        data used for plots
    plot : JSInput
        plot javascript code
    output : Union[Path, str]
        output file name
    style : Union[str, dict]
        a file or a dictionary defining a CSS file
    grid : int
        number of columns
    scale_factor : float
        only for :code:`.png` file; the more the number is higher, the more the quality of image will be
    """
    if isinstance(output, str):
        output = Path(output)
    input = Path("~detroit-tmp.html")
    input.write_text(await html(data, plot, style=style, grid=grid, fetch=False, svg=output.suffix == ".svg"))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        if output.suffix == ".png":
            context = await browser.new_context(device_scale_factor=scale_factor)
            page = await context.new_page()
            await page.goto(f'file://{input.absolute()}')
            width = await page.evaluate_handle("width");
            height = await page.evaluate_handle("height");
            await page.set_viewport_size({'width': int(float(str(width))), 'height': int(float(str(height)))})
            await page.goto(f'file://{input.absolute()}')
            await page.screenshot(path=output, type='png')
        elif output.suffix == ".pdf":
            page = await browser.new_page()
            await page.goto(f'file://{input.absolute()}')
            await page.pdf(path=output)
        elif output.suffix == ".svg":
            page = await browser.new_page()
            await page.set_viewport_size({'width': 2560, 'height': 1440})
            await page.goto(f'file://{input.absolute()}')
            jshandle = await page.evaluate_handle("mysvg")
            output.write_text(str(jshandle))
        else:
            await browser.close()
            input.unlink()
            raise ValueError(f"Unsupported \"{output.suffix}\" file")
        await browser.close()
        input.unlink()

def save(data: DataInput, plot: JSInput, output:Union[Path, str], style:Union[str, dict]=None, grid:int=1, scale_factor:float=1) -> str:
    """
    Save the plot into a `output` file given arguments
    It supports :

    * :code:`.svg` files
    * :code:`.png` files
    * :code:`.pdf` files

    Parameters
    ----------
    data : DataInput
        data used for plots
    plot : JSInput
        plot javascript code
    output : Union[Path, str]
        output file name
    style : Union[str, dict]
        a file or a dictionary defining a CSS file
    grid : int
        number of columns
    scale_factor : float
        only for :code:`.png` file; the more the number is higher, the more the quality of image will be

    Returns
    -------
    str
        Message which confirms the save of the file

    Examples
    --------

    >>> df = pl.read_csv("barley.csv")
    >>> data = Data(arrange(df))
    >>> color = {"legend": js("true"), "label": "Elevation (m)"}
    >>> contour = Plot.contour(
    ...     data.values,
    ...     {
    ...         "width": data.width,
    ...         "height": data.height,
    ...         "fill": js("Plot.identity"),
    ...         "stroke": "black"
    ...     },
    ... )
    >>> plot = Plot.plot({"color": , "marks": [contour]})
    >>> save(df, plot, "figure.png", scale_factor=2)
    "figure.png" saved.
    """
    asyncio.run(_save(arrange(data), plot, output, style, grid, scale_factor))
    return f"{output} saved."

def render(data: DataInput, plot: JSInput, style:Union[Path, str]=None, grid:int=1):
    """
    Launch a web application to render plot. In a jupyter environment, display directly the plot.

    Parameters
    ----------
    data : DataInput
        data used for plots
    plot : JSInput
        plot javascript code
    style : Union[str, dict]
        a file or a dictionary defining a CSS file
    grid : int
        number of columns

    Examples
    --------

    >>> df = pl.read_csv("barley.csv")
    >>> data = Data(arrange(df))
    >>> color = {"legend": js("true"), "label": "Elevation (m)"}
    >>> contour = Plot.contour(
    ...     data.values,
    ...     {
    ...         "width": data.width,
    ...         "height": data.height,
    ...         "fill": js("Plot.identity"),
    ...         "stroke": "black"
    ...     },
    ... )
    >>> plot = Plot.plot({"color": , "marks": [contour]})
    >>> render(df, plot)
    """
    data = arrange(data)
    if JUPYTER_INSTALLED and jupyter_environment():
        display(
            HTML(asyncio.run(html(data, plot, style=style, fetch=False, grid=grid))),
            metadata={"isolated": True}
        )
    else:
        app = Quart("detroit")

        @app.route("/data")
        def get_data():
            return data

        @app.route("/")
        async def main():
            return await html(data, plot, style=style, fetch=True, grid=grid)

        app.run()
