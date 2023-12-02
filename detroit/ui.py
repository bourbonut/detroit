from .svg import SVG_SCRIPT
from quart import Quart, render_template, request
from quart.app import _cancel_all_tasks
from markupsafe import Markup
from threading import Thread
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
from jinja2 import Environment, PackageLoader, select_autoescape

FETCH = Markup("var data;fetch(\"/data\").then(response => response.json()).then(d => {data = d;})")

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

async def html(data, plot, fetch=True, svg=False):
    env = Environment(loader=PackageLoader("detroit"), autoescape=select_autoescape(), enable_async=True)
    template = env.get_template("index.html")
    return await template.render_async(
        javascript_code=Markup(plot),
        get_data=FETCH if fetch else Markup(f"const data = {data};"),
        get_svg=Markup(SVG_SCRIPT) if svg else ""
    )

def start_service(data, plot, svg=False):
    app = Quart("detroit")

    @app.route("/data")
    def get_data():
        return data

    if svg:
        @app.route("/svg", methods=["POST"])
        async def get_svg():
            svg = (await request.get_data()).decode()
            with open("figure.svg", "w") as file:
                file.write(svg)
            return svg

    @app.route("/")
    async def main():
        return await html(data, plot, fetch=True)

    app.run()

def save(data, plot, output, scale_factor=1, width=640, height=440):
    asyncio.run(_save(data, plot, output, scale_factor, width, height))

def render(data, javascript_code):
    start_service(data, javascript_code)
