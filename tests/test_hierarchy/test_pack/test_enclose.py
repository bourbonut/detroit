import detroit as d3

def test_enclose():
    circles = [
      {"x": 14.5, "y": 48.5, "r": 7.585},
      {"x": 9.5, "y": 79.5, "r": 2.585},
      {"x": 15.5, "y": 73.5, "r": 8.585},
    ]
    enclose = d3.pack_enclose(circles)
    assert {
        "x": round(enclose.x, 6),
        "y": round(enclose.y, 6),
        "r": round(enclose.r, 6),

    } == {
        "r": round(20.790781637717107, 6),
        "x": round(12.80193548387092, 6),
        "y": round(61.59615384615385, 6),
    }
