from jinja2 import Environment, FileSystemLoader, select_autoescape
from quart import Quart, render_template

from detroit import Plot, js

WORLD_URL = "https://static.observableusercontent.com/files/7c6167b65013c12f3978b4d8e85dd28a27e3b5eb580d1e76696ce5b0d399c196de2b02c45e734462931e1af823698e36bb072722253d5e03e7fb61222755bc0c"


async def load_template(**variables):
    """
    Load "templates/main.js", change some variables, and save it into "static/main.js"
    """
    loader = FileSystemLoader("./templates")
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    template = env.get_template("main.js")
    with open("static/main.js", "w") as file:
        file.write(await template.render_async(**variables))


app = Quart(__name__)


@app.route("/")
async def main():
    plot = Plot.plot(
        {
            "projection": {"type": "orthographic", "rotate": [js("-longitude"), -30]},
            "r": {
                "transform": js("(d) => Math.pow(10, d)")
            },  # convert Richter to amplitude
            "style": "overflow: visible;",  # allow dots to escape
            "marks": [
                Plot.geo(js("land"), {"fill": "currentColor", "fillOpacity": 0.2}),
                Plot.sphere(),
                Plot.dot(
                    js("earthquakes"),
                    {
                        "x": "longitude",
                        "y": "latitude",
                        "r": "magnitude",
                        "stroke": "red",
                        "fill": "red",
                        "fillOpacity": 0.2,
                    },
                ),
            ],
        }
    )
    await load_template(plot=str(plot), url=WORLD_URL)
    return await render_template("index.html")


if __name__ == "__main__":
    app.run()
