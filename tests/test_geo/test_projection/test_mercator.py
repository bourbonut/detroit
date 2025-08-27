import detroit as d3


def test_mercator_1():
    projection = (
        d3.geo_mercator()
        .translate([0, 0])
        .scale(1)
        .set_clip_extent(None)
        .set_precision(0)
    )
    assert (
        d3.geo_path(projection).set_digits(6)({"type": "Sphere"})
        == "M3.141593,-3.141593L3.141593,0L3.141593,3.141593L3.141593,3.141593L-3.141593,3.141593L-3.141593,3.141593L-3.141593,0L-3.141593,-3.141593L-3.141593,-3.141593L3.141593,-3.141593Z"
    )
    assert projection.get_clip_extent() is None


def test_mercator_2():
    projection = (
        d3.geo_mercator()
        .translate([0, 0])
        .scale(1)
        .set_center([10, 10])
        .set_precision(0)
    )
    assert (
        d3.geo_path(projection).set_digits(6)({"type": "Sphere"})
        == "M2.96706,-2.966167L2.96706,0.175426L2.96706,3.317018L2.96706,3.317018L-3.316126,3.317018L-3.316126,3.317019L-3.316126,0.175426L-3.316126,-2.966167L-3.316126,-2.966167L2.96706,-2.966167Z"
    )
    assert projection.get_clip_extent() is None


def test_mercator_3():
    projection = (
        d3.geo_mercator()
        .translate([0, 0])
        .scale(1)
        .set_clip_extent([[-10, -10], [10, 10]])
        .set_precision(0)
    )
    assert (
        d3.geo_path(projection).set_digits(6)({"type": "Sphere"})
        == "M3.141593,-10L3.141593,0L3.141593,10L3.141593,10L-3.141593,10L-3.141593,10L-3.141593,0L-3.141593,-10L-3.141593,-10L3.141593,-10Z"
    )
    assert projection.get_clip_extent() == [[-10, -10], [10, 10]]


def test_mercator_4():
    projection = (
        d3.geo_mercator()
        .translate([0, 0])
        .set_clip_extent([[-10, -10], [10, 10]])
        .scale(1)
        .set_precision(0)
    )
    assert (
        d3.geo_path(projection).set_digits(6)({"type": "Sphere"})
        == "M3.141593,-10L3.141593,0L3.141593,10L3.141593,10L-3.141593,10L-3.141593,10L-3.141593,0L-3.141593,-10L-3.141593,-10L3.141593,-10Z"
    )
    assert projection.get_clip_extent() == [[-10, -10], [10, 10]]


def test_mercator_5():
    projection = (
        d3.geo_mercator()
        .scale(1)
        .set_clip_extent([[-10, -10], [10, 10]])
        .translate([0, 0])
        .set_precision(0)
    )
    assert (
        d3.geo_path(projection).set_digits(6)({"type": "Sphere"})
        == "M3.141593,-10L3.141593,0L3.141593,10L3.141593,10L-3.141593,10L-3.141593,10L-3.141593,0L-3.141593,-10L-3.141593,-10L3.141593,-10Z"
    )
    assert projection.get_clip_extent() == [[-10, -10], [10, 10]]


def test_mercator_6():
    projection = d3.geo_mercator()
    obj = {
        "type": "MultiPoint",
        "coordinates": [
            [-82.35024908550241, 29.649391549778745],
            [-82.35014449996858, 29.65075946917633],
            [-82.34916073446641, 29.65070265688781],
            [-82.3492653331286, 29.64933474064504],
        ],
    }
    projection.fit_extent([[0, 0], [960, 600]], obj)
    assert projection.get_scale() == 20969742.365692537
    assert projection.get_translation() == [30139734.76760269, 11371473.949706702]
    projection.rotate([0, 95]).fit_extent([[0, 0], [960, 600]], obj)
    assert projection.get_scale() == 35781690.650920525
    assert projection.get_translation() == [75115911.95344561, 2586046.4116968135]
