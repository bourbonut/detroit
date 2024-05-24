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

# {{{
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
            if next_content.contents:
                if next_content.contents[0].name not in {"svg", "p"}:
                    yield code_section(next_content)
        elif next_content.name == "p":
            yield format_paragraph(next_content.text)
        elif next_content.name == "h2":
            break
        current_index += 1

async def get_docstring(method, client):
    response = await client.get(method.url)
    soup = BeautifulSoup(response.text, "lxml")
    id_ = method.url.split("#")[-1]
    id_ = "namespaces-1" if id_ == "namespaces" else id_
    h2 = soup.find("h2", {"id": id_})
    if h2:
        return list(extract(h2))
    else:
        h3 = soup.find("h3", {"id": method.url.split("#")[-1]})
        return list(extract(h3))

# }}}

def get_methods():
    """
    Get methods from the API index
    """
    response = httpx.get("https://d3js.org/api")
    soup = BeautifulSoup(response.text, "lxml")
    for ul in soup.find("main", {"class": "main"}).find_all("ul"):
        yield (
            Method(link.text, f"https://d3js.org{link['href'][1:]}")
            for link in ul.find_all("a")
        )

async def make_method(method, client):
    try:

        strings = await get_docstring(method, client)
        valid_subclass = "." in method.name and "d3" not in method.name
        subclass = method.name.split(".")[0] if valid_subclass else None
        head = strings.pop(0).replace("new ", "").replace(" \u200b", "")
        if subclass:
            head = head.replace(f"{subclass}.", "")
            subclass = subclass.replace("adder", "Adder")
        signature = SIGNATURE.match(head)
        if signature is None:
            name = head.split(" ^")[0]
            args = ""
            format_args = ""
        elif "..." in head:
            name = signature[1]
            args = signature[2]
            format_args = args.replace("...", "")
            args = args.replace("...", "*")
        else:
            name = signature[1]
            format_args = signature[2]
            args = ", ".join((f"{arg}=None" for arg in format_args.split(", "))) if format_args else ""
            if format_args:
                format_args = f"({format_args})" if "," in format_args else f"({format_args},)"
        docstring = "\n\n".join(strings) + f"\nSee more informations `here` <{method.url}>`_."
        docstring = "\n        ".join(docstring.split("\n"))
        return name, args, format_args, docstring, subclass

    except Exception as e:
        print(method)
        print(e)

async def gather_all(groups):
    result = []
    async with httpx.AsyncClient() as client:
        for methods in groups:
            result.extend(await asyncio.gather(*map(make_method, methods, repeat(client))))
    return result

def groupby(methods):
    d = {subclass: [] for _, _, _, _, subclass in methods if subclass}
    d[None] = []
    for name, args, format_args, docstring, subclass in methods:
        if subclass or name in d:
            d[subclass or name].append((name, args, format_args, docstring))
        else:
            d[subclass].append((name, args, format_args, docstring))
    for subclass, methods in d.items():
        if len(methods) > 1 and methods[0][0] == methods[1][0]:
            docstring = "\n\n        ".join((methods[0][3], methods[1][3]))
            name = methods[1][0]
            args = methods[1][1]
            format_args = methods[1][2]
            d[subclass] = d[subclass][2:]
            d[subclass].insert(0, (name, args, format_args, docstring))
    return d

async def test_make_template():
    loader = FileSystemLoader([Path("scrapper/templates")])
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    groups = get_methods()
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    # next(groups)
    methods = await gather_all([next(groups)])
    subclasses = groupby(methods)
    # __import__('pprint').pprint(methods)
    # __import__('pprint').pprint(subclasses)

    template = env.get_template("d3_subclass.py")
    for subclass in subclasses.keys() - {None}:
        result = await template.render_async(methods=subclasses[subclass][1:], class_name=subclass)
        # print(result)
        with open(f"/tmp/{subclass.lower()}.py", "w") as file:
            file.write(result)

    template = env.get_template("d3.py")
    methods = subclasses[None]
    subclasses = [subclasses[key][0] for key in subclasses.keys() - {None}]
    result = await template.render_async(methods=methods, subclasses=subclasses)
    # print(result)
    with open("/tmp/d3.py", "w") as file:
        file.write(result)

async def make_template():
    loader = FileSystemLoader([Path("scrapper/templates")])
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    # for group in get_methods():
    #     for method in group:
    #         print(method)
    methods = await gather_all(get_methods())
    subclasses = groupby(methods)
    # print(subclasses.keys())

    template = env.get_template("d3_subclass.py")
    for subclass in subclasses.keys() - {None}:
        result = await template.render_async(methods=subclasses[subclass][1:], class_name=subclass)
        with open(f"/tmp/{subclass.lower()}.py", "w") as file:
            file.write(result)

    template = env.get_template("d3.py")
    methods = subclasses[None]
    subclasses = [subclasses[key][0] for key in subclasses.keys() - {None}]
    result = await template.render_async(methods=methods, subclasses=subclasses)
    with open("/tmp/d3.py", "w") as file:
        file.write(result)

async def main():
    async with httpx.AsyncClient() as client:
        for string in (await make_method(Method(name='pie.padAngle', url='https://d3js.org/d3-shape/pie#pie_padAngle'), client)):
            print(f"{string!r}")

asyncio.run(make_template())
