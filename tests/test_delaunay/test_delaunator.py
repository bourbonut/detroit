from detroit.delaunay.delaunator import Delaunator
from functools import reduce
from operator import iadd
from pathlib import Path
import json
import pytest

DATAPATH = Path(__file__).resolve().parent / "data"

def ssum(x):
    sum_value = x[0]
    err = 0
    for i in range(1, len(x)):
        k = x[i]
        m = sum_value + k
        err += sum_value - m + k if abs(sum_value) >= abs(k) else k - m + sum_value
        sum_value = m

    return sum_value + err

def orient(p, r, q):
    px, py = p
    rx, ry = r
    qx, qy = q
    u = (ry - py) * (qx - px)
    r = (rx - px) * (qy - py)
    return abs(u - r) >= (u - r if 3.3306690738754716e-16 * abs(u + r) else 0)

def convex(r, q, p):
    return (orient(p, r, q) or orient(r, q, p) or orient(q, p, r)) >= 0

def validate(points, d = None):
    d = Delaunator.from_points(points) if d is None else d
    for i in range(len(d.halfedges)):
        assert d.halfedges[i] == -1 or d.halfedges[d.halfedges[i]] == i

    hull_areas = []
    length = len(d.hull)
    j = length - 1
    for i in range(length):
        x0, y0 = points[d.hull[j]]
        x, y = points[d.hull[i]]
        hull_areas.append((x - x0) * (y + y0))
        assert convex(
            points[d.hull[j]],
            points[d.hull[(j + 1) % length]],
            points[d.hull[(j + 3) % length]]
        )
        j = i

    hull_area = ssum(hull_areas)

    triangle_areas = []
    for i in range(0, len(d.triangles), 3):
        ax, ay = points[d.triangles[i]]
        bx, by = points[d.triangles[i + 1]]
        cx, cy = points[d.triangles[i + 2]]
        triangle_areas.append(abs((by - ay) * (cx - bx) - (bx - ax) * (cy - by)))

    triangle_area = ssum(triangle_areas)

    err = abs((hull_area - triangle_area) / hull_area)
    assert err <= 2 ** -51

@pytest.fixture
def points():
    return json.loads((DATAPATH / "ukraine.json").read_text())

@pytest.fixture
def issue13():
    return json.loads((DATAPATH / "issue13.json").read_text())

@pytest.fixture
def issue43():
    return json.loads((DATAPATH / "issue43.json").read_text())

@pytest.fixture
def issue44():
    return json.loads((DATAPATH / "issue44.json").read_text())

@pytest.fixture
def robustness1():
    return json.loads((DATAPATH / "robustness1.json").read_text())

@pytest.fixture
def robustness2():
    return json.loads((DATAPATH / "robustness2.json").read_text())

@pytest.fixture
def robustness3():
    return json.loads((DATAPATH / "robustness3.json").read_text())

@pytest.fixture
def robustness4():
    return json.loads((DATAPATH / "robustness4.json").read_text())

def test_delaunator_1(points):
    d = Delaunator(reduce(iadd, points, []))
    assert d.triangles == Delaunator.from_points(points).triangles

def test_delaunator_2():
    with pytest.raises(ValueError):
        Delaunator([])

def test_delaunator_3(points):
    with pytest.raises(TypeError):
        Delaunator(points)

def test_delaunator_4(points):
    validate(points)

def test_delaunator_5(points):
    d = Delaunator.from_points(points)
    validate(points, d)
    assert len(d) == 3573 # it should be 5133

    p = [80, 220]
    d.coords[0] = p[0]
    d.coords[1] = p[1]
    new_points = [p] + points[1:]

    d.update()
    validate(new_points, d)
    assert len(d) == 3888 # it should be 5139

def test_delaunator_6():
    validate([[516, 661], [369, 793], [426, 539], [273, 525], [204, 694], [747, 750], [454, 390]])

def test_delaunator_7(issue13):
    validate(issue13)

def test_delaunator_8():
    validate([[382, 302], [382, 328], [382, 205], [623, 175], [382, 188], [382, 284], [623, 87], [623, 341], [141, 227]])

def test_delaunator_9(issue43):
    validate(issue43)

def test_delaunator_10(issue44):
    validate(issue44)

@pytest.mark.parametrize(
    "transform", [
        lambda p: p,
        lambda p: [p[0] / 1e9, p[1] / 1e9],
        lambda p: [p[0] / 100, p[1] / 100],
        lambda p: [p[0] * 100, p[1] * 100],
        lambda p: [p[0] * 1e9, p[1] * 1e9],
    ]
)
def test_delaunator_11(transform, robustness1):
    validate(list(map(transform, robustness1)))

def test_delaunator_12(robustness2):
    validate(robustness2[0:100])

@pytest.mark.skip
def test_delaunator_13(robustness2):
    validate(robustness2)

def test_delaunator_14(robustness3):
    validate(robustness3)

def test_delaunator_15(robustness4):
    validate(robustness4)

def test_delaunator_16():
    d = Delaunator.from_points([[0, 0], [1, 0], [3, 0], [2, 0]])
    assert d.triangles == []
    assert d.hull == [0, 1, 3, 2]

def test_delaunator_17():
    d = Delaunator.from_points(
        [{"x": 5, "y": 5}, {"x": 7, "y": 5}, {"x": 7, "y": 6}],
        lambda p: p["x"],
        lambda p: p["y"],
    )
    assert d.triangles == [0, 2, 1]
