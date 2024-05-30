from bs4 import BeautifulSoup

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
