import detroit as d3
from detroit.hierarchy.pack.enclose import Circle
from math import sqrt
import pytest

def swap(array, i, j):
    array[i], array[j] = array[j], array[i]

def permute(array, f, n = None):
    if n is None:
        n = len(array)
    if n == 1:
        f(array)
        return
    for i in range(n - 1):
        permute(array, f, n - 1)
        swap(array, 0 if n & 1 else i, n - 1)
    permute(array, f, n - 1)

def circle_value(value):
    return Circle.from_other(
        {'r': sqrt(value)}
    )

def circle_radius(radius):
    return Circle.from_other(
        {'r': radius}
    )

def intersects_any(circles):
    n = len(circles)
    for i in range(n):
        ci = circles[i]
        for j in range(i + 1, n):
            if intersects(ci, circles[j]):
                return True
    return False

def intersects(a, b):
    dr = a.r + b.r - 1e-6
    dx = b.x - a.x
    dy = b.y - a.y
    return dr > 0 and dr * dr > dx * dx + dy * dy

@pytest.mark.parametrize(
    "radii", [
        [100, 200, 500, 70, 4],
        [3, 30, 50, 400, 600],
        [1, 1, 3, 30, 50, 400, 600],
    ]
)
def test_siblings_1(radii):
    permute(
        [circle_value(x) for x in radii],
        lambda p: not (intersects_any(d3.pack_siblings(p)) and [c.r for c in p])
    )

@pytest.mark.parametrize(
    "circle_func, radii",
    [
        (
            circle_value,
            [
                2,
                9071,
                79,
                51,
                325,
                867,
                546,
                19773,
                371,
                16,
                165781,
                10474,
                6928,
                40201,
                31062,
                14213,
                8626,
                12,
                299,
                1075,
                98918,
                4738,
                664,
                2694,
                2619,
                51237,
                21431,
                99,
                5920,
                1117,
                321,
                519162,
                33559,
                234,
                4207,
            ]
        ),
        (
            circle_radius,
            [
                0.3371386860049076,
                58.65337373332081,
                2.118883785686244,
                1.7024669121097333,
                5.834919697833051,
                8.949453403094978,
                6.792586534702093,
                105.30490014617664,
                6.058936212213754,
                0.9535722042975694,
                313.7636051642043,
            ],
        ),
        (
            circle_radius,
            [
                6.26551789195159,
                1.707773433636342,
                9.43220282933871,
                9.298909705475646,
                5.753163715613753,
                8.882383159012575,
                0.5819319661882536,
                2.0234859171687747,
                2.096171518434433,
                9.762727931304937,
            ],
        ),
        (
            circle_radius,
            [
                9.153035316963035,
                9.86048622524424,
                8.3974499571329,
                7.8338007571397865,
                8.78260490259886,
                6.165829618300345,
                7.134819943097564,
                7.803701771392344,
                5.056638985134191,
                7.424601077645588,
                8.538658023474753,
                2.4616388562274896,
                0.5444633747829343,
                9.005740508584667,
            ]
        ),
        (
            circle_radius,
            [
                2.23606797749979,
                52.07088264296293,
                5.196152422706632,
                20.09975124224178,
                357.11557267679996,
                4.898979485566356,
                14.7648230602334,
                17.334875731491763,
            ],
        ),
        (
            circle_radius,
            [
                0.5672035864083508,
                0.6363498687452267,
                0.5628456216244132,
                1.5619458670239148,
                1.5658933259424268,
                0.9195955097595698,
                0.4747083763630309,
                0.38341282734497434,
                1.3475593361729394,
                0.7492342961633259,
                1.0716990115071823,
                0.31686823341701664,
                2.8766442376551415e-7,
            ]
        )
    ]
)
def test_siblings_2(circle_func, radii):
    assert intersects_any(d3.pack_siblings([circle_func(x) for x in radii])) is False

def test_siblings_3():
    assert [
        {"r": c.r, "x": c.x, "y": c.y}
        for c in d3.pack_siblings([circle_radius(x) for x in [1e+11, 1, 1]])
    ] == [
        {"r": 1e+11, "x": 0, "y": 0},
        {"r": 1, "x": 1e+11 + 1, "y": 0},
        {"r": 1, "x": 1e+11 + 1, "y": 2}
    ]

def test_siblings_4():
    assert [
        {"r": c.r, "x": c.x, "y": c.y}
        for c in d3.pack_siblings([circle_radius(x) for x in [1e+16, 1, 1]])
    ] == [
        {"r": 1e+16, "x": 0, "y": 0},
        {"r": 1, "x": 1e+16 + 1, "y": 0},
        {"r": 1, "x": 1e+16 + 1, "y": 2}
    ]
