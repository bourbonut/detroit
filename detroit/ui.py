import asyncio
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
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

from .utils import FETCH, random_id, wait_function, arrange
from .style import CSS, GRID

def jupyter_environment():
    try:
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except NameError:
        return False

async def html(data, plot, style=None, fetch=True, svg=None, grid=None):
    env = Environment(loader=PackageLoader("detroit"), autoescape=select_autoescape(), enable_async=True)
    style = CSS(style)
    if isinstance(plot, dict):
        template = env.get_template("grid.html")
        plot = {random_id(): {"title": title, "code": Markup(code)} for title, code in plot.items()}
        plot_id = None
        if svg is not None:
            for id in plot:
                if plot[id]["title"] == svg:
                    plot_id = f"plot-{id}"
                    break
        if grid is not None:
            style.update(GRID(grid))
        return await template.render_async(
            plot=plot,
            get_data=FETCH if fetch else Markup(f"const data = {data};"),
            get_svg=Markup(await wait_function(env, plot_id)) if plot_id else "",
            set_style=str(style),
        )
    template = env.get_template("simple.html")
    return await template.render_async(
        javascript_code=Markup(plot),
        get_data=FETCH if fetch else Markup(f"const data = {data};"),
        get_svg=Markup(await wait_function(env, "myplot")) if svg else "",
        set_style=str(style),
    )

async def _save(data, plot, output, style, grid, scale_factor, width, height, svg):
    if isinstance(output, str):
        output = Path(output)
    input = Path("~detroit-tmp.html")
    input.write_text(await html(data, plot, style=style, grid=grid, fetch=False, svg=svg or output.suffix == ".svg"))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        if output.suffix == ".png":
            context = await browser.new_context(device_scale_factor=scale_factor)
            page = await context.new_page()
            await page.set_viewport_size({'width': width, 'height': height})
            await page.goto(f'file://{input.absolute()}')
            await page.screenshot(path=output, type='png')
        elif output.suffix == ".pdf":
            page = await browser.new_page()
            await page.goto(f'file://{input.absolute()}')
            await page.pdf(path=output)
        elif output.suffix == ".svg":
            page = await browser.new_page()
            await page.goto(f'file://{input.absolute()}')
            jshandle = await page.evaluate_handle("mysvg")
            output.write_text(str(jshandle))
        else:
            await browser.close()
            input.unlink()
            raise ValueError(f"Unsupported \"{output.suffix}\" file")
        await browser.close()
        input.unlink()

def save(data, plot, output, style=None, grid=None, scale_factor=1, width=640, height=440, svg=None):
    asyncio.run(_save(arrange(data), plot, output, style, grid, scale_factor, width, height, svg))

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
            return await html(data, plot, style=style, fetch=True, grid=grid, svg=True)

        app.run()
