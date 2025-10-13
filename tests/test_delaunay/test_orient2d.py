from pathlib import Path

from detroit.delaunay.orient2d import orient2d, orient2dfast


def test_orient2d_1():
    assert orient2d(0, 0, 1, 1, 0, 1) < 0


def test_orient2d_2():
    assert orient2d(0, 0, 0, 1, 1, 1) > 0


def test_orient2d_3():
    assert orient2d(0, 0, 0.5, 0.5, 1, 1) == 0


def test_orient2d_4():
    assert orient2dfast(0, 0, 1, 1, 0, 1) < 0


def test_orient2d_5():
    assert orient2dfast(0, 0, 0, 1, 1, 1) > 0


def test_orient2d_6():
    assert orient2dfast(0, 0, 0.5, 0.5, 1, 1) == 0


def test_orient2d_7():
    datapath = Path(__file__).resolve().parent / "data" / "orient2d.txt"
    assert datapath.exists()
    for line in datapath.read_text().splitlines():
        _, ax, ay, bx, by, cx, cy, sign = map(float, line.split(" "))
        result = orient2d(ax, ay, bx, by, cx, cy)
        assert (-1.0 if result < 0.0 else 1.0) == -sign
