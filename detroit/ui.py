import asyncio
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Generator, List, Optional, Union

from markupsafe import Markup

from .d3_utils import Script
from .plot import Plot_
from .style import CSS, GRID
from .utils import Data, DataInput, arrange

JSCode = Union[Plot_, Script]
JSInput = Union[Dict[str, JSCode], List[JSCode]]

class PlotType(Enum):
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
    if isinstance(plot, Plot_):
        return PlotType.SINGLE_PLOT
    elif isinstance(plot, Script):
        return PlotType.SINGLE_D3
    elif isinstance(plot, dict):
        objs = plot.values()
        if all(map(lambda obj: isinstance(obj, Plot_), objs)):
            return PlotType.MULTIPLE_PLOTS
        elif all(map(lambda obj: isinstance(obj, Script), objs)):
            return PlotType.MULTIPLE_D3
    elif isinstance(plot, list):
        if all(map(lambda obj: isinstance(obj, Plot_), plot)):
            return PlotType.MULTIPLE_PLOTS
        elif all(map(lambda obj: isinstance(obj, Script), plot)):
            return PlotType.MULTIPLE_D3
    return PlotType.UNIDENTIFIED

async def html(data: dict, plot: JSInput, style:Union[Path, str, dict]=None, svg:bool=False, grid:int=1, event:Optional[str] = None, autoreload:bool = False) -> str:
    """
    Return HTML content filled by arguments from detroit templates

    Parameters
    ----------
    data : Union[dict, Generator[dict, None, None]]
        data used for plots
    plot : JSInput
        plot javascript code
    style : Union[Path, str, dict]
        a file or a dictionary defining a CSS file
    svg : bool
        True to get javascript functions to generate a svg object in javascript
    grid : int
        number of columns
    event: Optional[str]
        for dynamic update, this javascript code is inserted into the websocket updates
    autoreload : bool
        reload automatically your browser page

    Returns
    -------
    str
        HTML content filled by arguments
    """
    from jinja2 import (ChoiceLoader, Environment, PackageLoader, select_autoescape)
    loader = ChoiceLoader([PackageLoader("detroit", "templates"), PackageLoader("detroit", "static")])
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    plot_type = identify(plot)
    style = CSS(style)

    if event: # dynamic updates
        if plot_type != PlotType.SINGLE_D3:
            raise TypeError("Unsupported plot for dynamic updates")
        code = Markup(plot)
        data = Markup(f"const data = {data};" if data else "const data = {};")
        template = env.get_template("websocket.html")
        return await template.render_async(
            code = code,
            data = data,
            style = str(style),
            event = Markup(event),
        )

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
        autoreload=autoreload,
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
    style : Union[Path, str, dict]
        a file or a dictionary defining a CSS file
    grid : int
        number of columns
    scale_factor : float
        only for :code:`.png` file; the more the number is higher, the more the quality of image will be
    """
    from playwright.async_api import async_playwright
    if isinstance(output, str):
        output = Path(output)
    input = Path("~detroit-tmp.html")
    input.write_text(await html(data, plot, style=style, grid=grid, svg=output.suffix == ".svg"))
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

def save(data: DataInput, plot: JSInput, output:Union[Path, str], style:Union[Path, str, dict]=None, grid:int=1, scale_factor:float=1) -> str:
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
    style : Union[Path, str, dict]
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

def websocket_save(
    generator: Generator[dict, None, None],
    script: Script,
    event: str,
    style:Union[Path, str, dict]=None,
    init_data: Optional[DataInput] = None,
    record_video_dir:str="videos/",
    time:int = 2000,
    width:int = 660,
    height:int = 420,
    verbose=False,
) -> str:
    """
    Record the rendering into a headless browser and
    save the video as :code:`.webm` in :code:`record_video_dir`.

    Parameters
    ----------
    generator : Generator[dict, None, None]
        generator function which return new updates of data
    script : Script
        plot javascript code (only d3 supported)
    event : str
        javascript code called during updates
    style : Union[Path, str, dict]
        a file or a dictionary defining a CSS file
    init_data : Optional[DataInput]
        initial data before updates
    record_video_dir : str
        directory where videos are saved
    time : int
        timeout to wait
    width : int
        width of the video
    height : int
        height of the video
    verbose :
        :code:`True` to enable logging

    Returns
    -------
    str
        Message which confirms the save of the file

    Examples
    --------

    Check :ref:`the full example<Update Guide>` for more information

    >>> websocket_save(
    ...     generator,
    ...     script,
    ...     event=js("update(received_data.values, received_data.xmax);"),
    ...     init_data=data,
    ... )
    """
    from quart import Quart, websocket
    from hypercorn.asyncio import serve
    from hypercorn import Config
    from playwright.async_api import async_playwright
    import logging

    if not verbose:
        logging.disable(logging.CRITICAL)

    app = Quart("detroit")

    @app.websocket("/ws")
    async def ws():
        for data in generator():
            await websocket.send_json(data)

    @app.route("/")
    async def main():
        return await html(data=arrange(init_data), plot=script, style=style, event=event)

    shutdown_event = asyncio.Event()
    async def local_save(url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(
                record_video_dir=record_video_dir,
                viewport={"width": width, "height": height}
            )
            page = await context.new_page()
            await page.goto(url)
            await page.wait_for_timeout(time)
            await page.close()
            await context.close()
            await browser.close()
        shutdown_event.set()

    config = Config()
    config.bind = ["localhost:5000"]

    loop = asyncio.get_event_loop()
    loop.create_task(local_save("http://localhost:5000"))
    loop.run_until_complete(
        serve(app, config, shutdown_trigger=shutdown_event.wait)
    )
    return f"Video saved."

def render(data: DataInput, plot: JSInput, style:Union[Path, str, dict]=None, grid:int=1, autoreload:bool=False):
    """
    Launch a web application to render plot. In a jupyter environment, display directly the plot.

    Parameters
    ----------
    data : DataInput
        data used for plots
    plot : JSInput
        plot javascript code
    style : Union[Path, str, dict]
        a file or a dictionary defining a CSS file
    grid : int
        number of columns
    autoreload : bool
        reload automatically your browser page

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
    from quart import Quart
    try:
        import nest_asyncio
        nest_asyncio.apply()
        from IPython import get_ipython
        from IPython.display import HTML, display
        JUPYTER_INSTALLED = True
    except:
        JUPYTER_INSTALLED = False
    data = arrange(data)
    if JUPYTER_INSTALLED and jupyter_environment():
        display(
            HTML(asyncio.run(html(data, plot, style=style, grid=grid))),
            metadata={"isolated": True}
        )
    else:
        app = Quart("detroit")

        @app.route("/data")
        def get_data():
            return data

        @app.route("/")
        async def main():
            return await html(data, plot, style=style, grid=grid, autoreload=autoreload)

        app.run()

def websocket_render(generator: Generator[dict, None, None], script: Script, event: str, style:Union[Path, str, dict]=None, init_data: Optional[DataInput] = None):
    """
    Launch a web application to render plot with dynamic updates of data
    Jupyter environment not supported

    Parameters
    ----------
    generator : Generator[dict, None, None]
        Generator function which return new updates of data
    script : Script
        Plot javascript code (only d3 supported)
    event : str
        Javascript code called during updates
    style : Union[Path, str, dict]
        A file or a dictionary defining a CSS file
    init_data : Optional[DataInput]
        Initial data before updates

    Examples
    --------

    Check :ref:`the full example<Update Guide>` for more information

    >>> update = function("data", "xmax", name="update")
    >>> update(d3(content="x").domain([0, js("xmax")]).nice())
    >>> update(svg.selectAll("g.xaxis").call(d3.axisBottom(x)))
    >>> update(
    ...     svg(content="line").datum(data)
    ...       .attr("d", d3.line()
    ...       .x(function("d").inline("x(d.x)"))
    ...       .y(function("d").inline("y(d.y)"))
    ...     )
    ... )
    >>> script(update)
    >>> def generator():
    ...     s = 1000
    ...     istep = 4 * pi / 1000
    ...     xv = [istep * i for i in range(1000)]
    ...     yv = list(map(sin, xv))
    ...     for i in range(1000):
    ...         xmax = istep * (s + i)
    ...         xv.append(xmax)
    ...         yv.append(sin(istep * (s + i)))
    ...         yield {"values": arrange([xv, yv]), "xmax": xmax}
    >>> websocket_render(
    ...     generator,
    ...     script,
    ...     event=js("update(received_data.values, received_data.xmax);"),
    ...     init_data=data
    ... )
    """
    from quart import Quart, websocket
    try:
        import nest_asyncio
        nest_asyncio.apply()
        from IPython import get_ipython
        from IPython.display import HTML, display
        JUPYTER_INSTALLED = True
    except:
        JUPYTER_INSTALLED = False
    if JUPYTER_INSTALLED and jupyter_environment():
        raise EnvironmentError("Dynamic updates in Jupyter environment unsupported")
    else:
        app = Quart("detroit")

        @app.websocket("/ws")
        async def ws():
            for data in generator():
                await websocket.send_json(data)

        @app.route("/")
        async def main():
            return await html(data=arrange(init_data), plot=script, style=style, event=event)

        app.run()
