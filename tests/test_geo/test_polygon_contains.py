import detroit as d3
from detroit.geo.polygon_contains import polygon_contains as contains
from math import radians

def ring_radians(ring):
    ring = list(map(point_radians, ring))
    ring.pop()
    return ring

def point_radians(point):
    return [radians(point[0]), radians(point[1])]

def polygon_contains(polygon, point):
    return contains(list(map(ring_radians, polygon)), point_radians(point))

def test_polygon_contains_1():
    assert polygon_contains([], [0, 0]) == 0

def test_polygon_contains_2():
    polygon = [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
    assert polygon_contains(polygon, [0.1, 2]) == 0
    assert polygon_contains(polygon, [0.1, 0.1]) == 1

def test_polygon_contains_3():
    polygon = d3.geo_circle().set_radius(60)()["coordinates"]
    assert polygon_contains(polygon, [-180, 0]) == 0
    assert polygon_contains(polygon, [1, 1]) == 1

def test_polygon_contains_4():
    polygon = d3.geo_circle().set_center([300, 0])()["coordinates"]
    assert polygon_contains(polygon, [300, 0]) == 1
    assert polygon_contains(polygon, [-60, 0]) == 1
    assert polygon_contains(polygon, [-420, 0]) == 1

def test_polygon_contains_5():
    polygon = [[[-60, -80], [60, -80], [180, -80], [-60, -80]]]
    assert polygon_contains(polygon, [0, 0]) == 0
    assert polygon_contains(polygon, [0, -85]) == 1
    assert polygon_contains(polygon, [0, -90]) == 1

def test_polygon_contains_6():
    polygon = [[[60, 80], [-60, 80], [-180, 80], [60, 80]]]
    assert polygon_contains(polygon, [0, 0]) == 0
    assert polygon_contains(polygon, [0, 85]) == 1
    assert polygon_contains(polygon, [0, 90]) == 1
    assert polygon_contains(polygon, [-100, 90]) == 1
    assert polygon_contains(polygon, [0, -90]) == 0

def test_polygon_contains_7():
    polygon = [[[0, -30], [120, -30], [0, -90], [0, -30]]]
    assert polygon_contains(polygon, [0, -90]) == 0
    assert polygon_contains(polygon, [-60, -90]) == 0
    assert polygon_contains(polygon, [60, -90]) == 0
    polygon2 = [[[0, 30], [-120, 30], [0, 90], [0, 30]]]
    assert polygon_contains(polygon2, [0, 90]) == 0
    assert polygon_contains(polygon2, [-60, 90]) == 0
    assert polygon_contains(polygon2, [60, 90]) == 0

def test_polygon_contains_8():
    polygon = [[[0, 0], [10, -40], [-10, -40], [0, 0]]]
    assert polygon_contains(polygon, [0,-40.2]) == 1
    assert polygon_contains(polygon, [0,-40.5]) == 0

def test_polygon_contains_9():
    polygon = [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    assert polygon_contains(polygon, [0.1, 0.1]) == 0
    assert polygon_contains(polygon, [2, 0.1]) == 1

def test_polygon_contains_10():
    polygon = [[[-60, 80], [60, 80], [180, 80], [-60, 80]]]
    assert polygon_contains(polygon, [0, 85]) == 0
    assert polygon_contains(polygon, [0, 0]) == 1

def test_polygon_contains_11():
    polygon = [[[60, -80], [-60, -80], [-180, -80], [60, -80]]]
    assert polygon_contains(polygon, [0, -85]) == 0
    assert polygon_contains(polygon, [0, 0]) == 1

def test_polygon_contains_12():
    polygon = d3.geo_circle().set_radius(120)()["coordinates"]
    assert polygon_contains(polygon, [-180, 0]) == 0
    assert polygon_contains(polygon, [-90, 0]) == 1

def test_polygon_contains_13():
    polygon = [[[-170, -1], [0, -1], [170, -1], [170, 1], [0, 1], [-170, 1], [-170, -1]]]
    assert polygon_contains(polygon, [0, 0]) == 0
    assert polygon_contains(polygon, [0, 20]) == 1

def test_polygon_contains_14():
    circle = d3.geo_circle().set_center([0, -90])
    ring0 = circle.set_radius(90 - 0.01)()["coordinates"][0]
    ring1 = circle.set_radius(90 + 0.01)()["coordinates"][0][::-1]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0, 0]) == 0
    assert polygon_contains(polygon, [0, -90]) == 1

def test_polygon_contains_15():
    circle = d3.geo_circle().set_center([0, -90])
    ring0 = circle.set_radius(90 + 0.01)()["coordinates"][0]
    ring1 = circle.set_radius(90 - 0.01)()["coordinates"][0][::-1]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0, -90]) == 0
    assert polygon_contains(polygon, [0, 0]) == 1

def test_polygon_contains_16():
    ring0 = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
    ring1 = [[0.4, 0.4], [0.6, 0.4], [0.6, 0.6], [0.4, 0.6], [0.4, 0.4]]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0.5, 0.5]) == 0
    assert polygon_contains(polygon, [0.1, 0.5]) == 1

def test_polygon_contains_17():
    ring0 = [[0, -10], [-120, -10], [120, -10], [0, -10]]
    ring1 = [[0, 10], [120, 10], [-120, 10], [0, 10]]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0, 20]) == 0
    assert polygon_contains(polygon, [0, 0]) == 1

def test_polygon_contains_18():
    ring0 = [[10, 10], [-10, 10], [-10, -10], [10, -10], [10, 10]][::-1]
    ring1 = [[170, 10], [170, -10], [-170, -10], [-170, 10], [170, 10]][::-1]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0, 90]) == 0
    assert polygon_contains(polygon, [0, 0]) == 1

def test_polygon_contains_19():
    ring0 = [[10, 10], [-10, 10], [-10, -10], [10, -10], [10, 10]]
    ring1 = [[170, 10], [170, -10], [-170, -10], [-170, 10], [170, 10]]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0, 0]) == 0
    assert polygon_contains(polygon, [0, 20]) == 1

def test_polygon_contains_20():
    ring0 = [[10, 10], [-10, 10], [-10, -10], [10, -10], [10, 10]]
    ring1 = [[0, 80], [120, 80], [-120, 80], [0, 80]]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0, 90]) == 0
    assert polygon_contains(polygon, [0, -90]) == 1

def test_polygon_contains_21():
    ring0 = [[10, 10], [-10, 10], [-10, -10], [10, -10], [10, 10]][::-1]
    ring1 = [[0, 80], [120, 80], [-120, 80], [0, 80]][::-1]
    polygon = [ring0, ring1]
    assert polygon_contains(polygon, [0, -90]) == 0
    assert polygon_contains(polygon, [0, 90]) == 1

def test_polygon_contains_22():
    polygon = [[[0, 0], [1, 0], [1, 3], [3, 3], [3, 1], [0, 1], [0, 0]]]
    assert polygon_contains(polygon, [15, 0.5]) == 0
    assert polygon_contains(polygon, [12, 2]) == 0
    assert polygon_contains(polygon, [0.5, 0.5]) == 1
    assert polygon_contains(polygon, [2, 2]) == 1

def test_polygon_contains_23():
    polygon = [[[-10, -80], [120, -80], [-120, -80], [10, -85], [10, -75], [-10, -75], [-10, -80]]]
    assert polygon_contains(polygon, [0, 0]) == 0
    assert polygon_contains(polygon, [0, -76]) == 1
    assert polygon_contains(polygon, [0, -89]) == 1

def test_polygon_contains_24():
    polygon = [[[-10, 80], [-10, 75], [10, 75], [10, 85], [-120, 80], [120, 80], [-10, 80]]]
    assert polygon_contains(polygon, [0, 0]) == 0
    assert polygon_contains(polygon, [0, 76]) == 1
    assert polygon_contains(polygon, [0, 89]) == 1

def test_polygon_contains_25():
    polygon = d3.geo_circle().set_radius(90)()["coordinates"]
    assert polygon_contains(polygon, [0, 0]) == 1

def test_polygon_contains_26():
    polygon = [[[180, -90], [-45, 0], [45, 0], [180, -90]]]
    assert polygon_contains(polygon, [-46, 0]) == 0
    assert polygon_contains(polygon, [0, 1]) == 0
    assert polygon_contains(polygon, [-90, -80]) == 0
    assert polygon_contains(polygon, [-44, 0]) == 1
    assert polygon_contains(polygon, [0, 0]) == 1
    assert polygon_contains(polygon, [0, -30]) == 1
    assert polygon_contains(polygon, [30, -80]) == 1

def test_polygon_contains_27():
    polygon = [[[-45, 0], [45, 0], [180, -90], [-45, 0]]]
    assert polygon_contains(polygon, [-46, 0]) == 0
    assert polygon_contains(polygon, [0, 1]) == 0
    assert polygon_contains(polygon, [-90, -80]) == 0
    assert polygon_contains(polygon, [-44, 0]) == 1
    assert polygon_contains(polygon, [0, 0]) == 1
    assert polygon_contains(polygon, [0, -30]) == 1
    assert polygon_contains(polygon, [30, -80]) == 1

def test_polygon_contains_28():
    polygon = [[[180, -90], [-135, 0], [135, 0], [180, -90]]]
    assert polygon_contains(polygon, [180, 0]) == 0
    assert polygon_contains(polygon, [150, 0]) == 0
    assert polygon_contains(polygon, [180, -30]) == 0
    assert polygon_contains(polygon, [150, -80]) == 0
    assert polygon_contains(polygon, [0, 0]) == 1
    assert polygon_contains(polygon, [180, 1]) == 1
    assert polygon_contains(polygon, [-90, -80]) == 1

def test_polygon_contains_29():
    polygon = [[[180, 90], [45, 0], [-45, 0], [180, 90]]]
    assert polygon_contains(polygon, [-90, 0]) == 0
    assert polygon_contains(polygon, [0, -1]) == 0
    assert polygon_contains(polygon, [0, -80]) == 0
    assert polygon_contains(polygon, [-90, 1]) == 0
    assert polygon_contains(polygon, [-90, 80]) == 0
    assert polygon_contains(polygon, [-44, 10]) == 1
    assert polygon_contains(polygon, [0, 10]) == 1
    assert polygon_contains(polygon, [30, 80]) == 1
