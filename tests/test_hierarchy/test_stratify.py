import pytest

import detroit as d3
from detroit.hierarchy.hierarchy import Node


def noparent(node):
    copy = {}
    for k in node.__dict__:
        match k:
            case "children":
                if node.children is not None:
                    copy["children"] = [noparent(x) for x in node.children]
            case "parent":
                pass
            case _:
                value = node.__dict__[k]
                if value is not None:
                    value = None if value == {} else value
                    copy[k] = value
    return copy


def test_stratify_1():
    s = d3.stratify()
    assert s.get_id()({"id": "foo"}) == "foo"
    assert s.get_parent_id()({"parent_id": "bar"}) == "bar"


def test_stratify_2():
    s = d3.stratify()
    root = s(
        [
            {"id": "a"},
            {"id": "aa", "parent_id": "a"},
            {"id": "ab", "parent_id": "a"},
            {"id": "aaa", "parent_id": "aa"},
        ]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 2,
        "data": {"id": "a"},
        "children": [
            {
                "id": "aa",
                "depth": 1,
                "height": 1,
                "data": {"id": "aa", "parent_id": "a"},
                "children": [
                    {
                        "id": "aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"id": "aaa", "parent_id": "aa"},
                    }
                ],
            },
            {
                "id": "ab",
                "depth": 1,
                "height": 0,
                "data": {"id": "ab", "parent_id": "a"},
            },
        ],
    }


def test_stratify_3():
    s = d3.stratify()
    root = s(
        [
            {"id": "aaa", "parent_id": "aa"},
            {"id": "aa", "parent_id": "a"},
            {"id": "ab", "parent_id": "a"},
            {"id": "a"},
        ]
    )
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 2,
        "data": {"id": "a"},
        "children": [
            {
                "id": "aa",
                "depth": 1,
                "height": 1,
                "data": {"id": "aa", "parent_id": "a"},
                "children": [
                    {
                        "id": "aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"id": "aaa", "parent_id": "aa"},
                    }
                ],
            },
            {
                "id": "ab",
                "depth": 1,
                "height": 0,
                "data": {"id": "ab", "parent_id": "a"},
            },
        ],
    }


def test_stratify_4():
    s = d3.stratify()
    root = s(
        [
            {"id": "aaa", "parent_id": "aa"},
            {"id": "ab", "parent_id": "a"},
            {"id": "aa", "parent_id": "a"},
            {"id": "a"},
        ]
    )
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 2,
        "data": {"id": "a"},
        "children": [
            {
                "id": "ab",
                "depth": 1,
                "height": 0,
                "data": {"id": "ab", "parent_id": "a"},
            },
            {
                "id": "aa",
                "depth": 1,
                "height": 1,
                "data": {"id": "aa", "parent_id": "a"},
                "children": [
                    {
                        "id": "aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"id": "aaa", "parent_id": "aa"},
                    }
                ],
            },
        ],
    }


def test_stratify_5():
    s = d3.stratify()
    root = s(
        (
            [
                {"id": "aaa", "parent_id": "aa"},
                {"id": "ab", "parent_id": "a"},
                {"id": "aa", "parent_id": "a"},
                {"id": "a"},
            ]
        )
    )
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 2,
        "data": {"id": "a"},
        "children": [
            {
                "id": "ab",
                "depth": 1,
                "height": 0,
                "data": {"id": "ab", "parent_id": "a"},
            },
            {
                "id": "aa",
                "depth": 1,
                "height": 1,
                "data": {"id": "aa", "parent_id": "a"},
                "children": [
                    {
                        "id": "aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"id": "aaa", "parent_id": "aa"},
                    }
                ],
            },
        ],
    }


def test_stratify_6():
    s = d3.stratify()
    root = s(
        [
            {"id": "a", "parent_id": ""},
            {"id": "aa", "parent_id": "a"},
            {"id": "ab", "parent_id": "a"},
            {"id": "aaa", "parent_id": "aa"},
        ]
    )
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 2,
        "data": {"id": "a", "parent_id": ""},
        "children": [
            {
                "id": "aa",
                "depth": 1,
                "height": 1,
                "data": {"id": "aa", "parent_id": "a"},
                "children": [
                    {
                        "id": "aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"id": "aaa", "parent_id": "aa"},
                    }
                ],
            },
            {
                "id": "ab",
                "depth": 1,
                "height": 0,
                "data": {"id": "ab", "parent_id": "a"},
            },
        ],
    }


def test_stratify_7():
    s = d3.stratify()
    root = s(
        [
            {"id": 0, "parent_id": None},
            {"id": 1, "parent_id": 0},
            {"id": 2, "parent_id": 0},
        ]
    )
    assert noparent(root) == {
        "id": "0",
        "depth": 0,
        "height": 1,
        "data": {"id": 0, "parent_id": None},
        "children": [
            {"id": "1", "depth": 1, "height": 0, "data": {"id": 1, "parent_id": 0}},
            {"id": "2", "depth": 1, "height": 0, "data": {"id": 2, "parent_id": 0}},
        ],
    }


def test_stratify_8():
    s = d3.stratify()
    with pytest.raises(RuntimeError) as excinfo:
        s([{"id": "a"}, {"id": "b"}])
    assert str(excinfo.value) == "Multiple roots"

    with pytest.raises(RuntimeError) as excinfo:
        s([{"id": "a", "parent_id": "a"}])
    assert str(excinfo.value) == "No root"

    with pytest.raises(RuntimeError) as excinfo:
        s([{"id": "a", "parent_id": "b"}, {"id": "b", "parent_id": "a"}])
    assert str(excinfo.value) == "No root"


def test_stratify_9():
    s = d3.stratify()
    with pytest.raises(RuntimeError) as excinfo:
        s([{"id": "root"}, {"id": "a", "parent_id": "a"}])
    assert str(excinfo.value) == "Cycle"
    with pytest.raises(RuntimeError) as excinfo:
        s(
            [
                {"id": "root"},
                {"id": "a", "parent_id": "b"},
                {"id": "b", "parent_id": "a"},
            ]
        )
    assert str(excinfo.value) == "Cycle"


def test_stratify_10():
    s = d3.stratify()
    with pytest.raises(ValueError) as excinfo:
        s(
            [
                {"id": "a"},
                {"id": "b", "parent_id": "a"},
                {"id": "b", "parent_id": "a"},
                {"id": "c", "parent_id": "b"},
            ]
        )
    assert str(excinfo.value) == "Ambiguous"


def test_stratify_11():
    s = d3.stratify()
    with pytest.raises(ValueError) as excinfo:
        s([{"id": "a"}, {"id": "b", "parent_id": "c"}])
    assert str(excinfo.value) == "Missing: 'c'"


def test_stratify_12():
    s = d3.stratify()
    root = s([{"id": "a"}, {"parent_id": "a"}, {"parent_id": "a"}])
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 1,
        "data": {"id": "a"},
        "children": [
            {"depth": 1, "height": 0, "data": {"parent_id": "a"}},
            {"depth": 1, "height": 0, "data": {"parent_id": "a"}},
        ],
    }


def test_stratify_13():
    s = d3.stratify()
    root = s(
        [
            {"id": "a", "parent_id": None},
            {"id": "b", "parent_id": "a"},
            {"id": "b", "parent_id": "a"},
        ]
    )
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 1,
        "data": {"id": "a", "parent_id": None},
        "children": [
            {"id": "b", "depth": 1, "height": 0, "data": {"id": "b", "parent_id": "a"}},
            {"id": "b", "depth": 1, "height": 0, "data": {"id": "b", "parent_id": "a"}},
        ],
    }


def test_stratify_14():
    s = d3.stratify()
    assert not hasattr(s([{"id": ""}]), "id")
    assert not hasattr(s([{"id": None}]), "id")
    assert not hasattr(s([{}]), "id")


def test_stratify_15():
    s = d3.stratify()
    o = {"parent_id": "a"}
    root = s([{"id": "a"}, o])
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 1,
        "data": {"id": "a"},
        "children": [{"depth": 1, "height": 0, "data": o}],
    }


def test_stratify_16():
    def foo(d):
        return d["foo"]

    s = d3.stratify().set_id(foo)
    root = s(
        [
            {"foo": "a"},
            {"foo": "aa", "parent_id": "a"},
            {"foo": "ab", "parent_id": "a"},
            {"foo": "aaa", "parent_id": "aa"},
        ]
    )
    assert s.get_id() == foo
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 2,
        "data": {"foo": "a"},
        "children": [
            {
                "id": "aa",
                "depth": 1,
                "height": 1,
                "data": {"foo": "aa", "parent_id": "a"},
                "children": [
                    {
                        "id": "aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"foo": "aaa", "parent_id": "aa"},
                    }
                ],
            },
            {
                "id": "ab",
                "depth": 1,
                "height": 0,
                "data": {"foo": "ab", "parent_id": "a"},
            },
        ],
    }


def test_stratify_17():
    s = d3.stratify()
    with pytest.raises(TypeError):
        s.set_id(42)
    with pytest.raises(TypeError):
        s.set_id("nope")


def test_stratify_18():
    def foo(d):
        return d.get("foo")

    s = d3.stratify().set_parent_id(foo)
    root = s(
        [
            {"id": "a"},
            {"id": "aa", "foo": "a"},
            {"id": "ab", "foo": "a"},
            {"id": "aaa", "foo": "aa"},
        ]
    )
    assert s.get_parent_id() == foo
    assert noparent(root) == {
        "id": "a",
        "depth": 0,
        "height": 2,
        "data": {"id": "a"},
        "children": [
            {
                "id": "aa",
                "depth": 1,
                "height": 1,
                "data": {"id": "aa", "foo": "a"},
                "children": [
                    {
                        "id": "aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"id": "aaa", "foo": "aa"},
                    }
                ],
            },
            {"id": "ab", "depth": 1, "height": 0, "data": {"id": "ab", "foo": "a"}},
        ],
    }


def test_stratify_19():
    s = d3.stratify()
    with pytest.raises(TypeError):
        s.set_parent_id(42)
    with pytest.raises(TypeError):
        s.set_parent_id("nope")


def test_stratify_20():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/"}, {"path": "/aa"}, {"path": "/ab"}, {"path": "/aa/aaa"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": {"path": "/"},
        "children": [
            {
                "id": "/aa",
                "depth": 1,
                "height": 1,
                "data": {"path": "/aa"},
                "children": [
                    {
                        "id": "/aa/aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/aa/aaa"},
                    }
                ],
            },
            {"id": "/ab", "depth": 1, "height": 0, "data": {"path": "/ab"}},
        ],
    }


def test_stratify_21():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/"}, {"path": "/d"}, {"path": "/d/123"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": {"path": "/"},
        "children": [
            {
                "id": "/d",
                "depth": 1,
                "height": 1,
                "data": {"path": "/d"},
                "children": [
                    {
                        "id": "/d/123",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/d/123"},
                    }
                ],
            }
        ],
    }


def test_stratify_22():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/"}, {"path": "//"}, {"path": "///"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": {"path": "/"},
        "children": [
            {
                "id": "//",
                "depth": 1,
                "height": 1,
                "data": {"path": "//"},
                "children": [
                    {"id": "///", "depth": 2, "height": 0, "data": {"path": "///"}}
                ],
            }
        ],
    }


def test_stratify_23():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/"}, {"path": "/d/"}, {"path": "/d/123/"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": {"path": "/"},
        "children": [
            {
                "id": "/d",
                "depth": 1,
                "height": 1,
                "data": {"path": "/d/"},
                "children": [
                    {
                        "id": "/d/123",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/d/123/"},
                    }
                ],
            }
        ],
    }


def test_stratify_24():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/"}, {"path": "/d/123"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": {"path": "/"},
        "children": [
            {
                "id": "/d",
                "depth": 1,
                "height": 1,
                "data": None,
                "children": [
                    {
                        "id": "/d/123",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/d/123"},
                    }
                ],
            }
        ],
    }


def test_stratify_25():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/"}, {"path": "/aa"}, {"path": "\\/ab"}, {"path": "/aa\\/aaa"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 1,
        "data": {"path": "/"},
        "children": [
            {"id": "/aa", "depth": 1, "height": 0, "data": {"path": "/aa"}},
            {"id": "/\\/ab", "depth": 1, "height": 0, "data": {"path": "\\/ab"}},
            {"id": "/aa\\/aaa", "depth": 1, "height": 0, "data": {"path": "/aa\\/aaa"}},
        ],
    }


def test_stratify_26():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/aa/aaa"}, {"path": "/ab"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": None,
        "children": [
            {"id": "/ab", "depth": 1, "height": 0, "data": {"path": "/ab"}},
            {
                "id": "/aa",
                "depth": 1,
                "height": 1,
                "data": None,
                "children": [
                    {
                        "id": "/aa/aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/aa/aaa"},
                    }
                ],
            },
        ],
    }


def test_stratify_27():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [
            {"path": "/aa/aaa", "number": 1},
            {"path": "/aa/aaa", "number": 2},
        ]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/aa",
        "depth": 0,
        "height": 1,
        "data": None,
        "children": [
            {
                "id": "/aa/aaa",
                "depth": 1,
                "height": 0,
                "data": {"path": "/aa/aaa", "number": 1},
            },
            {
                "id": "/aa/aaa",
                "depth": 1,
                "height": 0,
                "data": {"path": "/aa/aaa", "number": 2},
            },
        ],
    }


def test_stratify_28():
    with pytest.raises(ValueError) as excinfo:
        d3.stratify().set_path(lambda d: d["path"])(
            [
                {"path": "/aa"},
                {"path": "/aa"},
                {"path": "/aa/aaa"},
                {"path": "/aa/aaa"},
            ]
        )
    assert str(excinfo.value) == "Ambiguous"


def test_stratify_29():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": ""}, {"path": "aa"}, {"path": "ab"}, {"path": "aa/aaa"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": {"path": ""},
        "children": [
            {
                "id": "/aa",
                "depth": 1,
                "height": 1,
                "data": {"path": "aa"},
                "children": [
                    {
                        "id": "/aa/aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "aa/aaa"},
                    }
                ],
            },
            {"id": "/ab", "depth": 1, "height": 0, "data": {"path": "ab"}},
        ],
    }


def test_stratify_30():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/aa/"}, {"path": "/ab/"}, {"path": "/aa/aaa/"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": None,
        "children": [
            {
                "id": "/aa",
                "depth": 1,
                "height": 1,
                "data": {"path": "/aa/"},
                "children": [
                    {
                        "id": "/aa/aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/aa/aaa/"},
                    }
                ],
            },
            {"id": "/ab", "depth": 1, "height": 0, "data": {"path": "/ab/"}},
        ],
    }


def test_stratify_31():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/aa//"}, {"path": "/b"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 3,
        "data": None,
        "children": [
            {"id": "/b", "depth": 1, "height": 0, "data": {"path": "/b"}},
            {
                "id": "/aa",
                "depth": 1,
                "height": 2,
                "data": None,
                "children": [
                    {
                        "id": "/aa/",
                        "depth": 2,
                        "height": 1,
                        "data": None,
                        "children": [
                            {
                                "id": "/aa//",
                                "depth": 3,
                                "height": 0,
                                "data": {"path": "/aa//"},
                            }
                        ],
                    }
                ],
            },
        ],
    }


def test_stratify_32():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/aa/aaa"}, {"path": "/aa"}, {"path": "/ab"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": None,
        "children": [
            {
                "id": "/aa",
                "depth": 1,
                "height": 1,
                "data": {"path": "/aa"},
                "children": [
                    {
                        "id": "/aa/aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/aa/aaa"},
                    }
                ],
            },
            {"id": "/ab", "depth": 1, "height": 0, "data": {"path": "/ab"}},
        ],
    }


def test_stratify_33():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/ab"}, {"path": "/aa"}, {"path": "/aa/aaa"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": None,
        "children": [
            {"id": "/ab", "depth": 1, "height": 0, "data": {"path": "/ab"}},
            {
                "id": "/aa",
                "depth": 1,
                "height": 1,
                "data": {"path": "/aa"},
                "children": [
                    {
                        "id": "/aa/aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/aa/aaa"},
                    }
                ],
            },
        ],
    }


def test_stratify_34():
    root = d3.stratify().set_path(lambda d: d["path"])(
        [{"path": "/ab"}, {"path": "/aa"}, {"path": "/aa/aaa"}]
    )
    assert isinstance(root, Node)
    assert noparent(root) == {
        "id": "/",
        "depth": 0,
        "height": 2,
        "data": None,
        "children": [
            {"id": "/ab", "depth": 1, "height": 0, "data": {"path": "/ab"}},
            {
                "id": "/aa",
                "depth": 1,
                "height": 1,
                "data": {"path": "/aa"},
                "children": [
                    {
                        "id": "/aa/aaa",
                        "depth": 2,
                        "height": 0,
                        "data": {"path": "/aa/aaa"},
                    }
                ],
            },
        ],
    }
