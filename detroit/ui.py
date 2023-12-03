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
    from IPython.display import display, HTML
    JUPYTER_INSTALLED = True
except:
    JUPYTER_INSTALLED = False

from .svg import SVG_SCRIPT

FETCH = Markup("var data;fetch(\"/data\").then(response => response.json()).then(d => {data = d;})")

def jupyter_environment():
    try:
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except NameError:
        return False

async def html(data, plot, fetch=True, svg=False):
    env = Environment(loader=PackageLoader("detroit"), autoescape=select_autoescape(), enable_async=True)
    template = env.get_template("index.html")
    return await template.render_async(
        javascript_code=Markup(plot),
        get_data=FETCH if fetch else Markup(f"const data = {data};"),
        get_svg=Markup(SVG_SCRIPT) if svg else ""
    )

async def _save(data, plot, output, scale_factor, width, height):
    if isinstance(output, str):
        output = Path(output)
    input = Path("~detroit-tmp.html")
    input.write_text(await html(data, plot, fetch=False, svg=output.suffix == ".svg"))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        if output.suffix == ".png":
            context = await browser.new_context(device_scale_factor=scale_factor)
            page = await context.new_page()
            await page.set_viewport_size({'width': width, 'height': height})
            await page.goto(f'file://{input.absolute()}')
            await page.screenshot(path=output, type='png')
            await browser.close()
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

def save(data, plot, output, scale_factor=1, width=640, height=440):
    asyncio.run(_save(data, plot, output, scale_factor, width, height))


def render(data, plot):
    if JUPYTER_INSTALLED and jupyter_environment():
        display(HTML(asyncio.run(html(data, plot, fetch=False))), metadata={"isolated": True})
    else:
        app = Quart("detroit")

        @app.route("/data")
        def get_data():
            return data

        @app.route("/")
        async def main():
            return await html(data, plot, fetch=True)

        app.run()
