import detroit as d3
from detroit.path import Path
import math
import pytest

def test_path_1():
    p = d3.path()
    assert isinstance(p, Path)
    assert str(p) == ""

def test_path_2():
    p = d3.path()
    p.move_to(150, 50)
    assert str(p) == "M150,50"
    p.line_to(200, 100)
    assert str(p) == "M150,50L200,100"
    p.move_to(100, 50)
    assert str(p) == "M150,50L200,100M100,50"

def test_path_3():
    p = d3.path()
    p.move_to(150, 50)
    assert str(p) == "M150,50"
    p.close_path()
    assert str(p) == "M150,50Z"
    p.close_path()
    assert str(p) == "M150,50ZZ"

def test_path_4():
    p = d3.path()
    assert str(p) == ""
    p.close_path()
    assert str(p) == ""

def test_path_5():
    p = d3.path()
    p.move_to(150, 50)
    assert str(p) == "M150,50"
    p.line_to(200, 100)
    assert str(p) == "M150,50L200,100"
    p.line_to(100, 50)
    assert str(p) == "M150,50L200,100L100,50"

def test_path_6():
    p = d3.path()
    p.move_to(150, 50)
    assert str(p) == "M150,50"
    p.quadratic_curve_to(100, 50, 200, 100)
    assert str(p) == "M150,50Q100,50,200,100"

def test_path_7():
    p = d3.path()
    p.move_to(150, 50)
    assert str(p) == "M150,50"
    p.bezier_curve_to(100, 50, 0, 24, 200, 100)
    assert str(p) == "M150,50C100,50,0,24,200,100"

def test_path_8():
    p = d3.path()
    p.move_to(150, 100)
    with pytest.raises(ValueError):
        p.arc(100, 100, -50, 0, math.pi / 2)

def test_path_9():
    p = d3.path()
    p.arc(100, 100, 0, 0, math.pi / 2)
    assert str(p) == "M100,100"

def test_path_10():
    p = d3.path()
    p.move_to(0, 0)
    p.arc(100, 100, 0, 0, math.pi / 2)
    assert str(p) == "M0,0L100,100"

def test_path_11():
    p = d3.path()
    p.arc(100, 100, 0, 0, 0)
    assert str(p) == "M100,100"

def test_path_12():
    p = d3.path()
    p.arc(100, 100, 0, 0, 1e-16)
    assert str(p) == "M100,100"

def test_path_13():
    p1 = d3.path()
    p1.arc(100, 100, 50, 0, math.pi * 2)
    assert str(p1) == "M150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"
    p2 = d3.path()
    p2.arc(0, 50, 50, -math.pi / 2, 0)
    assert str(p2) == "M0,0A50,50,0,0,1,50,50"

def test_path_14():
    p = d3.path()
    p.move_to(100, 100)
    p.arc(100, 100, 50, 0, math.pi * 2)
    assert str(p) == "M100,100L150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"

def test_path_15():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, math.pi / 2)
    assert str(p) == "M150,100A50,50,0,0,1,100,150"

def test_path_16():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, math.pi * 1)
    assert str(p) == "M150,100A50,50,0,1,1,50,100"

def test_path_17():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, math.pi * 2)
    assert str(p) == "M150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"

def test_path_18():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, math.pi / 2, False)
    assert str(p) == "M150,100A50,50,0,0,1,100,150"

def test_path_19():
    p = d3.path()
    p.move_to(100, 50)
    p.arc(100, 100, 50, -math.pi / 2, 0, False)
    assert str(p) == "M100,50A50,50,0,0,1,150,100"

def test_path_20():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 1e-16, True)
    assert str(p) == "M150,100A50,50,0,1,0,50,100A50,50,0,1,0,150,100"

def test_path_21():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 1e-16, False)
    assert str(p) == "M150,100"

def test_path_22():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, -1e-16, True)
    assert str(p) == "M150,100"

def test_path_23():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, -1e-16, False)
    assert str(p) == "M150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"

def test_path_24():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 2 * math.pi, True)
    assert str(p) == "M150,100A50,50,0,1,0,50,100A50,50,0,1,0,150,100"

def test_path_25():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 2 * math.pi, False)
    assert str(p) == "M150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"

def test_path_26():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 2 * math.pi + 1e-13, True)
    assert str(p) == "M150,100A50,50,0,1,0,50,100A50,50,0,1,0,150,100"

def test_path_27():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 2 * math.pi - 1e-13, False)
    assert str(p) == "M150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"

def test_path_28():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 2 * math.pi, True)
    assert str(p) == "M150,100A50,50,0,1,0,50,100A50,50,0,1,0,150,100"

def test_path_29():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 2 * math.pi, False)
    assert str(p) == "M150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"

def test_path_30():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 13 * math.pi / 2, False)
    assert str(p) == "M150,100A50,50,0,1,1,50,100A50,50,0,1,1,150,100"

def test_path_31():
    p = d3.path()
    p.move_to(100, 150)
    p.arc(100, 100, 50, 13 * math.pi / 2, 0, False)
    assert str(p) == "M100,150A50,50,0,1,1,150,100"

def test_path_32():
    p = d3.path()
    p.move_to(100, 150)
    p.arc(100, 100, 50, math.pi / 2, 0, False)
    assert str(p) == "M100,150A50,50,0,1,1,150,100"

def test_path_33():
    p = d3.path()
    p.move_to(100, 50)
    p.arc(100, 100, 50, 3 * math.pi / 2, 0, False)
    assert str(p) == "M100,50A50,50,0,0,1,150,100"

def test_path_34():
    p = d3.path()
    p.move_to(100, 50)
    p.arc(100, 100, 50, 15 * math.pi / 2, 0, False)
    assert str(p) == "M100,50A50,50,0,0,1,150,100"

def test_path_35():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, math.pi / 2, True)
    assert str(p) == "M150,100A50,50,0,1,0,100,150"

def test_path_36():
    p = d3.path()
    p.move_to(100, 50)
    p.arc(100, 100, 50, -math.pi / 2, 0, True)
    assert str(p) == "M100,50A50,50,0,1,0,150,100"

def test_path_37():
    p = d3.path()
    p.move_to(100, 50)
    p.arc(100, 100, 50, -13 * math.pi / 2, 0, True)
    assert str(p) == "M100,50A50,50,0,1,0,150,100"

def test_path_38():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, -13 * math.pi / 2, False)
    assert str(p) == "M150,100A50,50,0,1,1,100,50"

def test_path_39():
    p = d3.path()
    p.move_to(150, 100)
    p.arc(100, 100, 50, 0, 13 * math.pi / 2, True)
    assert str(p) == "M150,100A50,50,0,1,0,100,150"

def test_path_40():
    p = d3.path()
    p.move_to(100, 150)
    p.arc(100, 100, 50, math.pi / 2, 0, True)
    assert str(p) == "M100,150A50,50,0,0,0,150,100"

def test_path_41():
    p = d3.path()
    p.move_to(100, 50)
    p.arc(100, 100, 50, 3 * math.pi / 2, 0, True)
    assert str(p) == "M100,50A50,50,0,1,0,150,100"

def test_path_42():
    for true_like in [1, "1", True, 10, "3", "string"]:
        p = d3.path()
        p.move_to(100, 150)
        p.arc(100, 100, 50, math.pi / 2, 0, true_like)
        assert str(p) == "M100,150A50,50,0,0,0,150,100"

def test_path_43():
    for false_like in [0, None, None]:
        p = d3.path()
        p.move_to(150, 100)
        p.arc(100, 100, 50, 0, math.pi / 2, false_like)
        assert str(p) == "M150,100A50,50,0,0,1,100,150"

def test_path_44():
    p = d3.path()
    p.move_to(150, 100)
    with pytest.raises(ValueError):
        p.arc_to(270, 39, 163, 100, -53)

def test_path_45():
    p = d3.path()
    p.arc_to(270, 39, 163, 100, 53)
    assert str(p) == "M270,39"

def test_path_46():
    p = d3.path()
    p.move_to(270, 39)
    p.arc_to(270, 39, 163, 100, 53)
    assert str(p) == "M270,39"

def test_path_47():
    p = d3.path()
    p.move_to(100, 50)
    p.arc_to(101, 51, 102, 52, 10)
    assert str(p) == "M100,50L101,51"

def test_path_48():
    p = d3.path()
    p.move_to(100, 50)
    p.arc_to(101, 51, 101, 51, 10)
    assert str(p) == "M100,50L101,51"

def test_path_49():
    p = d3.path()
    p.move_to(270, 182), p.arc_to(270, 39, 163, 100, 0)
    assert str(p) == "M270,182L270,39"

def test_path_50():
    p1 = d3.path()
    p1.move_to(270, 182)
    p1.arc_to(270, 39, 163, 100, 53)
    assert str(p1) == "M270,182L270,130.223A53,53,0,0,0,190.751,84.179"
    p2 = d3.path()
    p2.move_to(270, 182)
    p2.arc_to(270, 39, 363, 100, 53)
    assert str(p2) == "M270,182L270,137.147A53,53,0,0,1,352.068,92.83"

def test_path_51():
    p = d3.path()
    p.move_to(100, 100), p.arc_to(200, 100, 200, 200, 100)
    assert str(p) == "M100,100A100,100,0,0,1,200,200"

def test_path_52():
    p = d3.path()
    p.move_to(100, 100), p.arc_to(200, 100, 200, 200, 50)
    p.arc(150, 150, 50, 0, math.pi)
    assert str(p) == "M100,100L150,100A50,50,0,0,1,200,150A50,50,0,1,1,100,150"

def test_path_53():
    p = d3.path()
    p.move_to(150, 100), p.rect(100, 200, 50, 25)
    assert str(p) == "M150,100M100,200h50v25h-50Z"
