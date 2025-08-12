from typing import Union

import pytest
from lxml import etree

import detroit as d3
from detroit.selection.enter import EnterNode


@pytest.fixture
def root():
    return etree.Element("svg", attrib={"xmlns": "http://www.w3.org/2000/svg"})


def subnode(parent: Union[etree.Element, etree.SubElement], node: str):
    subnode = etree.SubElement(parent, node)
    parent.append(subnode)
    return subnode


def to_string(node, pretty_print: bool = False):
    return (
        etree.tostring(node, pretty_print=pretty_print)
        .decode("utf-8")
        .removesuffix("\n")
    )


@pytest.fixture
def g_classes():
    svg = d3.create("svg")
    svg.select_all("g").data(list(range(10))).enter().append("g").attr(
        "class", lambda d: f"class{d}"
    ).append("text")
    return svg


def test_selection_1():
    svg = d3.create("svg")
    assert svg.to_string(False) == '<svg xmlns="http://www.w3.org/2000/svg"/>'
    assert len(svg._groups) == 1
    assert len(svg._groups[0]) == 1
    assert len(svg._parents) == 1
    assert svg._groups[0][0] == svg._parents[0]
    assert len(svg._data) == 0


def test_selection_2():
    svg = d3.create("svg")
    g = svg.append("g")
    assert len(g._groups) == 1
    assert len(g._groups[0]) == 1
    assert len(g._parents) == 1
    assert g._groups[0][0].tag == "g"
    assert str(svg) == '<svg xmlns="http://www.w3.org/2000/svg"><g/></svg>'
    assert len(svg._data) == 1


def test_selection_3(root):
    svg = d3.create("svg")
    text = svg.select_all("g").data([None] * 10).enter().append("g").append("text")
    assert len(text._groups) == 10
    assert len(text._groups[0]) == 1
    assert len(text._parents) == 10
    assert len(text._data) == 10 * 2
    for i in range(10):
        assert text._groups[i][0].tag == "text"
        assert text._parents[i].tag == "g"

        g = subnode(root, "g")
        subnode(g, "text")

    assert str(svg) == to_string(root)


def test_selection_4(g_classes):
    g = g_classes.select("g")
    assert g.node().tag == "g"
    assert g.node().attrib.get("class") == "class0"


def test_selection_5(g_classes):
    with pytest.raises(ValueError):
        g_classes.select("g:last")


def test_selection_6(g_classes):
    g = g_classes.select("g:last-of-type")
    assert g.node().tag == "g"
    assert g.node().attrib.get("class") == "class9"


def test_selection_7(g_classes):
    g = g_classes.select(".class0")
    assert g.node().tag == "g"
    assert g.node().attrib.get("class") == "class0"


def test_selection_8(g_classes):
    g = g_classes.select(".class")
    assert len(g._groups) == 1
    assert len(g._groups[0]) == 0


def test_selection_9(g_classes):
    text = g_classes.select("text")
    assert text.node().tag == "text"


def test_selection_10(g_classes):
    g = g_classes.select_all("g")
    nodes = g.nodes()
    assert len(nodes) == 10
    for i, node in enumerate(nodes):
        assert node.tag == "g"
        assert node.attrib.get("class") == f"class{i}"
    assert len(g._groups) == 1
    assert len(g._groups[0]) == 10
    assert len(g._parents) == 1


def test_selection_11(g_classes):
    text = g_classes.select_all("text")
    nodes = text.nodes()
    assert len(nodes) == 10
    for i, node in enumerate(nodes):
        assert node.tag == "text"
    assert len(text._groups) == 10
    for i in range(10):
        assert len(text._groups[i]) == 1
    assert len(text._parents) == 10


def test_selection_12():
    svg = d3.create("svg")
    svg.select_all("g").data([None] * 10).enter().append("g").attr(
        "class", lambda d: f"class"
    ).append("text")
    g = svg.select_all(".class")
    nodes = g.nodes()
    assert len(nodes) == 10
    for i, node in enumerate(nodes):
        assert node.tag == "g"
        assert node.attrib.get("class") == "class"
    assert len(g._groups) == 1
    assert len(g._groups[0]) == 10
    assert len(g._parents) == 1


def test_selection_13(g_classes):
    g = g_classes.select_all("g:last-of-type")
    nodes = g.nodes()
    assert len(nodes) == 1
    for i, node in enumerate(nodes):
        assert node.tag == "g"
        assert node.attrib.get("class") == "class9"
    assert len(g._groups) == 1
    assert len(g._groups[0]) == 1
    assert len(g._parents) == 1


def test_selection_14():
    data = ["hello", "world"]
    svg = d3.create("svg")
    text = svg.select_all("text").data(data)
    text_enter = text.enter()
    assert len(text_enter._groups[0]) == 2
    for i, enter_node in enumerate(text_enter._groups[0]):
        assert isinstance(enter_node, EnterNode)
        assert enter_node._parent == text_enter._parents[0]
        assert enter_node.__data__ == data[i]


def test_selection_15():
    data = ["hello", "world"]
    svg = d3.create("svg")
    text = svg.select_all("text").data(data)
    text_exit = text.exit()
    assert len(text_exit._groups) == 1
    assert len(text_exit._groups[0]) == 0
    assert text_exit._parents == svg._parents


def test_selection_16(root):
    data = ["hello", "world"]
    svg = d3.create("svg")
    text = svg.select_all("text").data(data)
    text_enter = text.enter()
    text_enter.append("text").text(lambda text: text)
    text = text.merge(text_enter)
    assert len(text_enter._groups[0]) == 2
    for i, enter_node in enumerate(text._groups[0]):
        assert isinstance(enter_node, EnterNode)
        assert enter_node._parent == text_enter._parents[0]
        assert enter_node.__data__ == data[i]

    text = subnode(root, "text")
    text.text = "hello"
    text = subnode(root, "text")
    text.text = "world"

    assert str(svg) == to_string(root)


def test_selection_17(g_classes):
    g = g_classes.select_all("g").filter(lambda d, i: i % 2 == 0)
    for i, node in enumerate(g.nodes()):
        assert node.attrib.get("class") == f"class{2 * i}"


def test_selection_18(g_classes):
    data = []

    def test(node, d, i, nodes):
        data.append((d, i))
        assert node in nodes

    g_classes.each(test)
    assert data == [(None, 0)]


def test_selection_19(g_classes):
    data = []

    def test(node, d, i, nodes):
        data.append((d, i))
        assert node in nodes

    g_classes.select_all("g").each(test)
    assert data == [(None, i) for i in range(10)]


def test_selection_20():
    svg = d3.create("svg")
    text = svg.append("text").attr("fill", "red")
    assert text.attr("fill") == "red"


def test_selection_21(root):
    svg = d3.create("svg")
    text = svg.append("text").attr("fill", "red")

    text = subnode(root, "text")
    text.set("fill", "red")
    assert str(svg) == to_string(root)


def test_selection_22():
    svg = d3.create("svg")
    text = svg.append("text").style("fill", "red").style("stroke", "none")
    assert text.style("fill") == "red"
    assert text.style("stroke") == "none"


def test_selection_23(root):
    svg = d3.create("svg")
    text = svg.append("text").style("fill", "red").style("stroke", "none")
    assert text.style("fill") == "red"
    assert text.style("stroke") == "none"

    text = subnode(root, "text")
    text.set("style", "fill:red;stroke:none;")
    assert str(svg) == to_string(root)


def test_selection_24():
    svg = d3.create("svg")
    text = svg.append("text").text("hello world")
    assert text.text() == "hello world"


def test_selection_25(root):
    svg = d3.create("svg")
    text = svg.append("text").text("hello world")

    text = subnode(root, "text")
    text.text = "hello world"
    assert str(svg) == to_string(root)


def test_selection_26():
    svg = d3.create("svg")
    g = (
        svg.select_all("g")
        .data(list(range(10)))
        .enter()
        .append("g")
        .attr("class", lambda d: f"class-{d}")
    )
    for i, node in enumerate(g.nodes()):
        assert node.attrib.get("class") == f"class-{i}"


def test_selection_27(root):
    svg = d3.create("svg")
    g = (
        svg.select_all("g")
        .data(list(range(10)))
        .enter()
        .append("g")
        .attr("class", lambda d: f"class-{d}")
    )

    for i in range(10):
        g = subnode(root, "g")
        g.set("class", f"class-{i}")

    assert str(svg) == to_string(root)

def test_selection_28():
    svg = d3.create("svg")
    text = (
        svg.select_all("text")
        .data(list(range(10)))
        .enter()
        .append("text")
        .style("fill", "red")
        .style("stroke", "none")
    )
    for i, node in enumerate(text.nodes()):
        assert node.attrib.get("style") == "fill:red;stroke:none;"


def test_selection_29(root):
    svg = d3.create("svg")
    text = (
        svg.select_all("text")
        .data(list(range(10)))
        .enter()
        .append("text")
        .style("fill", "red")
        .style("stroke", "none")
    )

    for i in range(10):
        text = subnode(root, "text")
        text.set("style", "fill:red;stroke:none;")

    assert str(svg) == to_string(root)

def test_selection_30():
    svg = d3.create("svg")
    text = (
        svg.select_all("text")
        .data(list(range(10)))
        .enter()
        .append("text")
        .text(lambda d: str(d))
    )
    for i, node in enumerate(text.nodes()):
        assert node.text == str(i)


def test_selection_31(root):
    svg = d3.create("svg")
    text = (
        svg.select_all("text")
        .data(list(range(10)))
        .enter()
        .append("text")
        .text(lambda d: str(d))
    )

    for i in range(10):
        text = subnode(root, "text")
        text.text = str(i)

    assert str(svg) == to_string(root)

def test_selection_32():
    svg = d3.create("svg")
    g1 = svg.append("g").attr("class", "g1")
    g2 = svg.append("g").attr("class", "g2")
    g = svg.select_all("g")
    g.datum("Hello, world")
    assert g._data[g1.node()] == "Hello, world"

def test_selection_33():
    data = ["Hello", "world"]
    svg = d3.create("svg")
    svg.append("g")
    svg.append("g")
    text = svg.select_all("text").data(data)
    assert len(text._enter) == 1
    assert len(text._enter[0]) == 2

    for i, enter_node in enumerate(text._enter[0]):
        assert isinstance(enter_node, EnterNode)
        assert enter_node._parent == svg._parents[0]
        assert enter_node.__data__ == data[i]

    for key, d in text._data.items():
        assert key.tag == "g"
        assert d is None

def test_selection_34():
    data = ["Hello", "world"]
    svg = d3.create("svg")
    svg.append("g")
    svg.append("g")
    g = svg.select_all("g").data(data)
    assert len(g._enter) == 1
    assert len(g._enter[0]) == 2

    for enter_node in g._enter[0]:
        assert enter_node is None

    for key, d in g._data.items():
        assert key.tag == "g"
        assert d in data
    

def test_selection_35(root):
    data = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    svg = d3.create("svg")
    table = (
        svg.append("table")
        .select_all("tr")
        .data(data)
        .join("tr")
        .select_all("td")
        .data(lambda _, d: d)
        .join("td")
        .text(lambda d: str(d))
    )

    table = subnode(root, "table")
    for di in data:
        tr = subnode(table, "tr")
        for d in di:
            td = subnode(tr, "td")
            td.text = str(d)

    assert str(svg) == to_string(root)

def test_selection_36(root):
    svg = d3.create("svg")
    data = [None] * 3
    svg.append("circle").attr("fill", "yellow")
    (
        svg.select_all("circle")
        .data(data)
        .join(
            onenter=lambda enter: enter.append("circle").attr("fill", "green"),
            onupdate=lambda update: update.attr("fill", "blue")
        )
        .attr("stroke", "black")
    )

    circle = subnode(root, "circle")
    circle.set("fill", "blue")
    circle = subnode(root, "circle")
    circle.set("fill", "green")
    circle.set("stroke", "black")
    circle = subnode(root, "circle")
    circle.set("fill", "green")
    circle.set("stroke", "black")

    assert str(svg) == to_string(root)

def test_selection_37(root):
    svg = d3.create("svg")
    (
        svg.select_all("g")
        .data([None, None])
        .enter()
        .append("g")
        .append("text")
    )
    svg.insert("circle", "text")

    for i in range(2):
        g = subnode(root, "g")
        subnode(g, "circle")
        subnode(g, "text")

    assert str(svg) == to_string(root)

def test_selection_38(root):
    svg = d3.create("svg")
    (
        svg.select_all("g")
        .data(["class1", "class2"])
        .enter()
        .append("g")
        .append("text")
        .attr("class", lambda d: d)
    )
    svg.insert("circle", ".class1")

    g = subnode(root, "g")
    subnode(g, "circle")
    text = subnode(g, "text")
    text.set("class", "class1")
    g = subnode(root, "g")
    text = subnode(g, "text")
    text.set("class", "class2")

    assert str(svg) == to_string(root)

def test_selection_39(root):
    svg = d3.create("svg")
    g = (
        svg.select_all("g")
        .data([None] * 10)
        .enter()
        .append("g")
        .attr("class", "domain")
    )
    assert len(g._groups[0]) == 10
    assert len(g._data) == 10

    g = svg.select_all(".domain").remove()
    assert len(g._groups[0]) == 0
    assert len(g._data) == 0

    assert str(svg) == to_string(root)

def test_selection_40():
    svg = d3.create("svg")
    box = []
    def test(svg, a, b, c):
        box.append(a)
        box.append(b)
        box.append(c)
    
    assert svg.call(test, 1, 2, 3) == svg
    assert box[0] == 1
    assert box[1] == 2
    assert box[2] == 3

@pytest.mark.skip
def test_selection_41():
    svg = d3.create("svg")
    svg2 = svg.clone()
    svg.append("g")
    assert str(svg) != str(svg2)

def test_selection_42():
    svg = d3.create("svg")
    svg.append("g").attr("class", "group1")
    svg.append("g").attr("aria-label", "group2")
    svg.append("g").attr("aria-label", "group2")
    s = svg.select("g[aria-label='group2']")
    assert s.node().tag == "g"
    assert s.node().attrib.get("aria-label") == "group2"

    s = svg.select_all("g[aria-label='group3']")
    assert len(s.nodes()) == 0

    s = svg.select_all("g[aria-label='group2']")
    assert len(s.nodes()) == 2

def test_selection_43():
    svg = d3.create("svg")
    svg.append("g").attr("aria-label", "group2").attr("transform", "translate(1, 0)")
    svg.append("g").attr("aria-label", "group2").attr("transform", "translate(0, 1)")

    s = svg.select_all("g[aria-label='group2']:last-of-type")
    assert len(s.nodes()) == 1
    assert s.node().attrib.get("transform") == "translate(0, 1)"

def test_selection_44():
    svg = d3.create("svg")
    svg.append("g").attr("aria-label", "group2")
    svg.append("rect").attr("aria-label", "group2")

    s = svg.select_all("[aria-label='group2']")
    assert len(s.nodes()) == 2
