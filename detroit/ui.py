from flask import Flask, render_template, request
from markupsafe import Markup

def download():
    import asyncio
    from playwright.async_api import async_playwright

    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(device_scale_factor=2)
            page = await context.new_page()
            await page.set_viewport_size({'width': 800, 'height': 600})
            await page.goto('localhost:5000')
            await page.screenshot(path='quality.png', type='png')
            await browser.close()

    asyncio.run(main())

def render(data, javascript_code):
    app = Flask(__name__)

    @app.route("/data")
    def get_data():
        return data

    @app.route("/svg", methods=["POST"])
    def get_svg():
        svg = request.data.decode()
        with open("figure.svg", "w") as file:
            file.write(svg)
        return svg

    @app.route("/")
    def main():
        return render_template(
            "index.html",
            javascript_code=Markup(javascript_code)
        )

    app.run()
