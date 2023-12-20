import asyncio
from pathlib import Path
from enum import Enum, auto

from jinja2 import Environment, ChoiceLoader, PackageLoader, select_autoescape
from markupsafe import Markup
from playwright.async_api import async_playwright
from quart import Quart, request

try:
    import nest_asyncio
    nest_asyncio.apply()
    from IPython import get_ipython
    from IPython.display import HTML, display
    JUPYTER_INSTALLED = True
except:
    JUPYTER_INSTALLED = False

from .utils import FETCH, load_svg_functions, arrange
from .style import CSS, GRID
from .d3 import Script
from .plot import Plot

class PlotType:
    SINGLE_PLOT = auto()
    MULTIPLE_PLOTS = auto()
    SINGLE_D3 = auto()
    MULTIPLE_D3 = auto()
    UNIDENTIFIED = auto()

def jupyter_environment():
    try:
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except NameError:
        return False

def identify(plot):
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
    return PlotType.UNIDENTIFIED

async def html(data, plot, style=None, fetch=True, svg=False, grid=None):
    loader = ChoiceLoader([PackageLoader("detroit", "templates"), PackageLoader("detroit", "static")])
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    plot_type = identify(plot)
    style = CSS(style)

    if plot_type == PlotType.UNIDENTIFIED:
        raise TypeError("Unsupported type of argument \"plot\"")
    elif plot_type == PlotType.MULTIPLE_D3 or plot_type == PlotType.MULTIPLE_PLOTS:
        single = False
        if grid is None:
            grid = 1
        else:
            style.update(GRID(grid))
        code = {
            id: {"title": title, "code": Markup(code)}
            for id, (title, code) in enumerate(plot.items())
        }
        id = f"plot-{len(plot) - 1}"
        width_code = "boundingRect.width"
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

    if plot_type == PlotType.SINGLE_D3 or plot_type == PlotType.MULTIPLE_D3:
        template = env.get_template("d3.html")
        data = Markup(f"const data = {data};")
    else:
        data = FETCH if fetch else Markup(f"const data = {data};")
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

async def _save(data, plot, output, style, grid, scale_factor, svg):
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

def save(data, plot, output, style=None, grid=None, scale_factor=1, svg=None):
    asyncio.run(_save(arrange(data), plot, output, style, grid, scale_factor, svg))
    return f"{output} saved."

def render(data, plot, style=None, grid=None):
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
