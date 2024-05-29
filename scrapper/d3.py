import httpx
from bs4 import BeautifulSoup
from collections import namedtuple
from itertools import repeat
from operator import contains
import re
import asyncio
import logging
import pickle

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

from scrapper.logging_config import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

Method = namedtuple("Method", ["name", "url"])
SIGNATURE = re.compile(r"\((.*)\)")

# {{{
def code_per_line(lines):
    """
    Return the code of each line
    """
    for span_line in lines:
        yield "".join((span.text for span in span_line.find_all("span")))

def code_section(content):
    """
    Return a code section
    """
    code = content.find("code")
    lines = code.find_all("span", {"class": "line"})
    embedded_code = "\n    ".join(code_per_line(lines))
    full_code = f""".. code:: javascript

    {embedded_code}
    """
    return full_code

def make_lines(words):
    """
    Split lines of docstring and apply 88 characters maximum per line
    """
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
    """
    Format a paragraph to fit 88 characters maximum
    """
    words = paragraph.split(" ")
    return "\n".join(make_lines(words))

def extract(header):
    """
    Extract different informations such as:
    - the signature of the function
    - the docstring
    """
    parent = header.parent
    yield header.text
    current_index = parent.index(header)
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
        return list(extract(h2)) + [f"\nSee more informations `here <{method.url}>`_."]
    else:
        h3 = soup.find("h3", {"id": method.url.split("#")[-1]})
        return list(extract(h3)) + [f"\nSee more informations `here <{method.url}>`_."]
# }}}

def get_methods():
    """
    Get methods from the API index
    """
    response = httpx.get("https://d3js.org/api")
    soup = BeautifulSoup(response.text, "lxml")
    # excluded_methods = ("back.", "elastic.", "poly.", "iterator", "cardinal.", "bundle.", "catmullRom.", "new d3.FormatSpecifier", "symbolType.")
    for ul in soup.find("main", {"class": "main"}).find_all("ul"):
        yield (
            Method(link.text, f"https://d3js.org{link['href'][1:]}")
            for link in ul.find_all("a") 
            # if not any(map(contains, repeat(link.text), excluded_methods))
        )

async def make_method(method, client):
    """
    Return informations useful to make a method
    """
    try:
        strings = await get_docstring(method, client)
        valid_subclass = "." in method.name and "d3" not in method.name
        subclass = method.name.split(".")[0] if valid_subclass else None
        head = strings.pop(0).replace("new ", "").replace(" \u200b", "")
        if subclass:
            head = head.replace(f"{subclass}.", "")
            subclass = subclass.replace("adder", "Adder")
        signature = SIGNATURE.match(head)
        if "[k]" in head:
            name = head.replace("[k]", "")
            args = ""
            format_args = ""
        elif signature is None:
            name = head.split(" ^")[0]
            args = ""
            format_args = ""
        elif "..." in head:
            name = signature[1]
            args = signature[2]
            format_args = args.replace("...", "")
            args = args.replace("...", "*")
        elif "blur2" in head:
            name = "blur2"
            args = "matrix=None, rx=None, ry=None"
            format_args = "(matrix, rx, ry)"
        else:
            name = signature[1]
            format_args = signature[2].replace("lambda", "lambda_")
            if "3" in format_args:
                args = format_args
                format_args = format_args.replace(" = 3", "")
            else:
                args = ", ".join((f"{arg} = None" for arg in format_args.split(", "))) if format_args else ""
            if format_args:
                format_args = f"({format_args})" if "," in format_args else f"({format_args},)"
        docstring = "\n\n".join(strings) + f"\nSee more informations `here <{method.url}>`_."
        docstring = "\n        ".join(docstring.split("\n"))
        return name, args, format_args, docstring, subclass

    except Exception as e:
        logger.error(method)
        logger.error(e.__traceback__())

async def gather_all(groups):
    """
    Gather results from groups of methods
    """
    result = []
    async with httpx.AsyncClient() as client:
        for methods in groups:
            result.extend(await asyncio.gather(*map(make_method, methods, repeat(client))))
    return result

def groupby(methods):
    """
    Group methods by their subclasses
    """
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

async def new_methods():
    results = []
    async with httpx.AsyncClient() as client:
        for methods in get_methods():
            methods = list(methods)
            docstrings = await asyncio.gather(*map(get_docstring, methods, repeat(client)))
            results.append(
                [
                    {"name": method.name, "url": method.url, "docstring": docstring}
                    for method, docstring in zip(methods, docstrings)
                ]
            )
    with open("results.pkl", "wb") as file:
        pickle.dump(results, file)


async def test_make_template():
    loader = FileSystemLoader([Path("scrapper/templates")])
    env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
    groups = get_methods()
    for methods in groups:
        methods = list(methods)
        if "d3-shape/symbol" in methods[0].url:
            break

    methods = await gather_all([methods])
    subclasses = groupby(methods)
    # __import__('pprint').pprint(methods)
    # __import__('pprint').pprint(subclasses)

    template = env.get_template("d3_subclass.py")
    for subclass in subclasses.keys() - {None}:
        result = await template.render_async(methods=subclasses[subclass][1:], class_name=subclass)
        print(result)
        # with open(f"/tmp/{subclass}.py", "w") as file:
        #     file.write(result)
    template = env.get_template("d3.py")
    methods = subclasses[None]
    subclasses = [subclasses[key][0] for key in subclasses.keys() - {None}]
    result = await template.render_async(methods=methods, subclasses=subclasses)
    print(result)
    # with open("/tmp/d3.py", "w") as file:
    #     file.write(result)

# def correction_voronoi(path):
#     content = path.read_text()
#     for correction in ("xmin", "ymin", "xmax", "ymax"):
#         content = re.sub(r"xminyminxmaxymax", correction, content, count=2)
#     content = re.sub(r"\(self, \)", r"(self)", content)
#     path.write_text(content)

# async def make_template():
#     loader = FileSystemLoader([Path("scrapper/templates")])
#     env = Environment(loader=loader, autoescape=select_autoescape(), enable_async=True)
#
#     methods = await gather_all(get_methods())
#     subclasses = groupby(methods)
#
#     template = env.get_template("d3_subclass.py")
#     for subclass in subclasses.keys() - {None}:
#         result = await template.render_async(methods=subclasses[subclass][1:], class_name=subclass)
#         with open(f"/tmp/{subclass}.py", "w") as file:
#             file.write(result)
#
#     template = env.get_template("d3.py")
#     methods = subclasses[None]
#     subclasses = [subclasses[key][0] for key in subclasses.keys() - {None}]
#     result = await template.render_async(methods=methods, subclasses=subclasses)
#     with open("/tmp/d3.py", "w") as file:
#         file.write(result)
#
#     correction_voronoi(Path("/tmp/voronoi.py"))

async def main():
    async with httpx.AsyncClient() as client:
        for string in (await make_method(Method(name='symbolType.draw', url='https://d3js.org/d3-shape/symbol#symbolType_draw'), client)):
            print(f"{string!r}")

# asyncio.run(new_methods())
# correction_voronoi()

def sort(methods):
    return sorted(
        filter(
            lambda m: "d3." in m["name"],
            methods
        ),
        key=lambda m: m["name"]
    ) + sorted(
        filter(
            lambda m: "d3." not in m["name"],
            methods
        ),
        key=lambda m: m["name"]
    )

def group_methods(sections):
    groups = []
    for methods in sections:
        group = {}
        for method in methods:
            insert(method, group)
        groups.append(group)
    return groups

def insert(method, group):
    name = method["name"]
    if "[" in name:
        return
    if "d3." in name:
        group[name] = {"_primary": method["docstring"]}
    elif "new" in name:
        name = name.replace("new ", "new d3.")
        group[name] = {"_primary": method["docstring"]}
    elif "." in name:
        prefix, suffix = name.split(".")
        found = False
        for method_name in group:
            if prefix.lower() in method_name.lower():
                group[method_name][suffix] = method["docstring"]
                found = True
        if not found:
            name = f"d3.{prefix}"
            group[name] = {"_primary": [f"{prefix}()", f"\nSee more informations `here <{method['url']}>`_."]}
            group[name][suffix] = method["docstring"]
    else:
        stop = False
        for method_name in group:
            if name.lower() in method_name.lower():
                docstring = group[method_name]["_primary"]
                docstring[0] = method["docstring"][0]
                docstring.extend(method["docstring"][1:])
                group[method_name]["_primary"] = docstring
                return

        name = f"d3.{name}"
        if name in group: # mix docstring
            docstring = group[name]["_primary"]
            docstring[0] = method["docstring"][0]
            docstring.extend(method["docstring"][1:])
            group[name]["_primary"] = docstring
        else:
            group[name] = {"_primary": method["docstring"]}

def remove_blank(line):
    no_blank = line.replace(" ", "")
    if not no_blank:
        return no_blank
    return line

def remove_first_blank(docstring):
    if not docstring[0] and len(docstring) > 1:
        docstring = docstring[1:]
        docstring[0] = docstring[0][8:]
        return docstring
    return docstring
    
def format_docstring(docstring):
    signature = docstring[0].replace("\u200b", "")
    docstring = "\n        ".join("\n".join(docstring[1:]).split("\n"))
    docstring = "\n".join(map(remove_blank, remove_first_blank(docstring.split("\n"))))
    match = SIGNATURE.findall(signature)
    if match:
        match = match[0] 
    if "[k]" in signature or not match:
        return "", "", docstring
    elif "..." in signature:
        args = match
        format_args = args.replace("...", "")
        args = args.replace("...", "*")
    elif "blur2" in signature:
        args = "matrix=None, rx=None, ry=None"
        format_args = "(matrix, rx, ry)"
    else:
        format_args = match.replace("lambda", "lambda_")
        if "3" in format_args:
            args = format_args.replace(" = 3", "=3")
            format_args = format_args.replace(" = 3", "")
        else:
            args = ", ".join((f"{arg}=None" for arg in format_args.split(", "))) if format_args else ""
        if format_args:
            format_args = f"({format_args})" if "," in format_args else f"({format_args},)"
    return args, format_args, docstring

def make_template():
    with open("results.pkl", "rb") as file:
        sections = pickle.load(file)

    groups = group_methods(sections)

    loader = FileSystemLoader([Path("scrapper/templates")])
    env = Environment(loader=loader, autoescape=select_autoescape())

    selection_groups = []
    locale = "d3.locale"
    selection = "d3.selection"
    for group in groups:
        contains_locale = locale in group.keys()
        if contains_locale and len(group[locale]) == 3:
            group["d3.format"]["_primary"].extend(group[locale]["format"][1:])
            group["d3.formatPrefix"]["_primary"].extend(group[locale]["formatPrefix"][1:])
            group.pop(locale)
        elif contains_locale and len(group[locale]) == 5:
            group["d3.timeFormat"]["_primary"].extend(group[locale]["format"][1:])
            group["d3.timeParse"]["_primary"].extend(group[locale]["parse"][1:])
            group["d3.utcFormat"]["_primary"].extend(group[locale]["utcFormat"][1:])
            group["d3.utcParse"]["_primary"].extend(group[locale]["utcParse"][1:])
            group.pop(locale)
        elif selection in group.keys():
            selection_groups.append(group.pop("d3.selection"))       


    mix_selection = {}
    for selection_methods in selection_groups:
        for method_name, docstring in selection_methods.items():
            if method_name in mix_selection:
                mix_selection[method_name].extend(docstring[1:])
            else:
                mix_selection[method_name] = docstring

    groups.append({"d3.selection": mix_selection})
    
    simple_methods = []
    subclasses = []
    submethods = {}
    # group = groups[59]
    # group = groups[-1]
    for i, group in enumerate(groups):
        for class_ in group:
            try:
                if len(group[class_]) == 1:
                    docstring = format_docstring(group[class_]["_primary"])
                    simple_methods.append((class_, *docstring))
                else:
                    docstring = format_docstring(group[class_]["_primary"])
                    subclasses.append((class_, *docstring))
                    methods_ = []
                    submethods[class_.replace("d3.", "").replace("new ", "")] = methods_
                    for method in group[class_]:
                        if method != "_primary":
                            docstring = format_docstring(group[class_][method])
                            methods_.append((method, *docstring))
            except Exception as e:
                print(class_, method, i)
                __import__('pprint').pprint(group[class_])
                print(e)
                raise

    d3_template = env.get_template("d3.py")
    subclass_template = env.get_template("d3_subclass.py")
    for class_, methods in submethods.items():
        result = subclass_template.render(methods=methods, class_name=class_)
        with open(f"/tmp/{class_}.py", "w") as file:
            file.write(result)

    result = d3_template.render(methods=simple_methods, subclasses=subclasses)
    with open("/tmp/d3.py", "w") as file:
        file.write(result)

make_template()
