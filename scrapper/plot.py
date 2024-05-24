import httpx
from bs4 import BeautifulSoup
from collections import namedtuple
from itertools import repeat
import re
import asyncio

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

Method = namedtuple("Method", ["name", "url"])
SIGNATURE = re.compile(r"([a-zA-Z0-9]*)\((.*)\)")

def get_methods():
    """
    Get methods from the API index
    """
    response = httpx.get("https://observablehq.com/plot/api")
    soup = BeautifulSoup(response.text, "lxml")
    for link in soup.find("main", {"class": "main"}).find("ul").find_all("a"):
        yield Method(link.text, f"https://observablehq.com/plot/{link['href']}")


def code_per_line(lines):
    for span_line in lines:
        yield "".join((span.text for span in span_line.find_all("span")))

def code_section(content):
    code = content.find("code")
    lines = code.find_all("span", {"class": "line"})
    embedded_code = "\n    ".join(code_per_line(lines))
    full_code = f""".. code:: javascript

    {embedded_code}
    """
    return full_code

def make_lines(words):
    total_count = 0
    line = ""
    for word in words:
        length = len(word) + 1
        if total_count + length > 88:
            yield line[:-1]
            line = word + " "
            total_count = length
        else:
            line += word + " "
            total_count += length
    yield line[:-1]

def format_paragraph(paragraph):
    words = paragraph.split(" ")
    return "\n".join(make_lines(words))


def extract(h2):
    parent = h2.parent
    yield h2.text
    current_index = parent.index(h2)
    while current_index < len(parent) - 1:
        next_content = parent.contents[current_index + 1]
        if next_content.name == "div":
            yield code_section(next_content)
        elif next_content.name == "p":
            yield format_paragraph(next_content.text)
        elif next_content.name == "h2":
            break
        current_index += 1

async def get_docstring(method, client):
    response = await client.get(method.url)
    soup = BeautifulSoup(response.text, "lxml")
    h2 = soup.find("h2", {"id": method.name})
    return list(extract(h2))

async def make_method(method, client):
    strings = await get_docstring(method, client)
    head = strings.pop(0)
    signature = SIGNATURE.match(head)
    if signature is None:
        name = head.split(" ^")[0]
        args = ""
        format_args = ""
    elif "..." in head:
        name = signature[1]
        args = signature[2]
        format_args = args.replace("...", "")
        # format_args = (f"', '.join(map(str, {arg.replace('...', '')}))" for arg in args.split(", ") if "..." in arg)
        # format_args = "{" + "}, {".join(format_args) + "}"
        args = args.replace("...", "*")
    else:
        name = signature[1]
        format_args = signature[2]
        # format_args = "{" + "}, {".join(args.split(", "))+ "}"
        args = ", ".join((f"{arg}=None" for arg in format_args.split(", ")))
    docstring = "\n".join(strings) + f"\nSee more informations `here` <{method.url}>`_."
    docstring = "\n        ".join(docstring.split("\n"))
    return (name, args, format_args, docstring)

# for string in get_docstring(Method("ruleX", "https://observablehq.com/plot/marks/rule#ruleX")):
#     print(string)

# full_method = make_method(Method("ruleX", "https://observablehq.com/plot/marks/rule#ruleX"))
async def make_template():
    loader = FileSystemLoader([Path("scrapper/templates")])
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    template = env.get_template("plot.py")
    methods = get_methods()
    async with httpx.AsyncClient() as client:
        methods = await asyncio.gather(*map(make_method, methods, repeat(client)))
    result = await template.render_async(methods=methods)
    with open("/tmp/plot.py", "w") as file:
        file.write(result)

async def main():
    async with httpx.AsyncClient() as client:
        for string in (await make_method(Method(name='marks', url='https://observablehq.com/plot/features/marks#marks'), client)):
            print(f"{string!r}")

# asyncio.run(make_template())
