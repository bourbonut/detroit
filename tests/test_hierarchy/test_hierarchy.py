import pytest

import detroit as d3


def test_hierarchy_1():
    root = d3.hierarchy(
        {
            "id": "root",
            "children": [{"id": "a"}, {"id": "b", "children": [{"id": "ba"}]}],
        }
    )
    a = root.children[0]
    b = root.children[1]
    ba = root.children[1].children[0]
    assert root.links() == [
        {"source": root, "target": a},
        {"source": root, "target": b},
        {"source": b, "target": ba},
    ]


def test_hierarchy_2():
    root = d3.hierarchy(
        {
            "id": "root",
            "children": [{"id": "a", "children": None}, {"id": "b", "children": 42}],
        }
    )
    a = root.children[0]
    b = root.children[1]
    assert root.links() == [
        {"source": root, "target": a},
        {"source": root, "target": b},
    ]


@pytest.fixture
def tree():
    return {
        "id": "root",
        "children": [
            {"id": "a", "children": [{"id": "ab"}]},
            {"id": "b", "children": [{"id": "ba"}]},
        ],
    }


def test_hierarchy_3(tree):
    root = d3.hierarchy(tree)
    a = []

    def foo(d):
        a.append(d.data["id"])

    root.each(foo)
    assert a == ["root", "a", "b", "ab", "ba"]


def test_hierarchy_4(tree):
    root = d3.hierarchy(tree)
    a = []

    def foo(d):
        a.append(d.data["id"])

    root.each_before(foo)
    assert a == ["root", "a", "ab", "b", "ba"]


def test_hierarchy_5(tree):
    root = d3.hierarchy(tree)
    a = []

    def foo(d):
        a.append(d.data["id"])

    root.each_after(foo)
    assert a == ["ab", "a", "ba", "b", "root"]


def test_hierarchy_6(tree):
    root = d3.hierarchy(tree)
    a = []

    def foo(d):
        a.append(d.data["id"])

    a = [d.data["id"] for d in root]
    assert a == ["root", "a", "b", "ab", "ba"]


def test_hierarchy_7():
    root = d3.hierarchy(
        {
            "id": "root",
            "children": [{"id": "a"}, {"id": "b", "children": [{"id": "ba"}]}],
        }
    ).count()

    def f1(d):
        return d.data["id"] == "b"

    assert root.find(f1).data["id"] == "b"

    def f2(d, i):
        return i == 0

    assert root.find(f2).data["id"] == "root"

    def f3(d, i, e):
        return d != e

    assert root.find(f3).data["id"] == "a"


def test_hierarchy_8():
    root = d3.hierarchy(
        {
            "id": "root",
            "children": [{"id": "a"}, {"id": "b", "children": [{"id": "ba"}]}],
        }
    ).count()
    assert root.copy().value == 2
