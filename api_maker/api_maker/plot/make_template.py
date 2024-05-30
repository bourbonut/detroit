from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

def make_template(methods):
    loader = FileSystemLoader([Path("api_maker/templates")])
    env = Environment(loader=loader, autoescape=select_autoescape())
    template = env.get_template("plot.py")
    result = template.render(methods=methods)
    with open("/tmp/plot.py", "w") as file:
        file.write(result)

