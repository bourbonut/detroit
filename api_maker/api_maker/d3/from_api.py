import httpx
from bs4 import BeautifulSoup
from collections import namedtuple
from itertools import repeat
import asyncio
import logging

logging.getLogger(__name__)

Method = namedtuple("Method", ["name", "url", "docstring"])

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
    """
    Get docstring of a method
    """
    response = await client.get(method.url)
    soup = BeautifulSoup(response.text, "lxml")
    id_ = method.url.split("#")[-1]
    id_ = "namespaces-1" if id_ == "namespaces" else id_
    header = soup.find("h2", {"id": id_}) or soup.find("h3", {"id": id_})
    docstring = list(extract(header)) + [f"\nSee more informations `here <{method.url}>`_."]
    return Method(method.name, method.url, docstring)

def get_methods():
    """
    Get methods from the API index
    """
    response = httpx.get("https://d3js.org/api")
    soup = BeautifulSoup(response.text, "lxml")
    for ul in soup.find("main", {"class": "main"}).find_all("ul"):
        yield (
            Method(link.text, f"https://d3js.org{link['href'][1:]}", None)
            for link in ul.find_all("a") 
        )

async def scrap_methods():
    """
    Scrap methods from the API index and return them
    """
    async with httpx.AsyncClient() as client:
        return [
            await asyncio.gather(*map(get_docstring, methods, repeat(client)))
            for methods in get_methods()
        ]
