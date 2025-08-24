import detroit as d3

def test_transverse_mercator_1():
    projection = d3.geo_transverse_mercator().translate([0, 0]).scale(1).set_clip_extent(None).set_precision(0)
    assert d3.geo_path(projection).set_digits(6)({"type": "Sphere"}) == "M3.141593,3.141593L0,3.141593L-3.141593,3.141593L-3.141593,-3.141593L-3.141593,-3.141593L0,-3.141593L3.141593,-3.141593L3.141593,3.141593Z"
    assert projection.get_clip_extent() is None

def test_transverse_mercator_2():
    projection = d3.geo_transverse_mercator().translate([0, 0]).scale(1).set_center([10, 10]).set_precision(0)
    assert d3.geo_path(projection).set_digits(6)({"type": "Sphere"}) == "M2.966167,3.316126L-0.175426,3.316126L-3.317018,3.316126L-3.317019,-2.967060L-3.317019,-2.967060L-0.175426,-2.967060L2.966167,-2.967060L2.966167,3.316126Z"
    assert projection.get_clip_extent() is None

def test_transverse_mercator_3():
    projection = d3.geo_transverse_mercator().translate([0, 0]).scale(1).set_clip_extent([[-10, -10], [10, 10]]).set_precision(0)
    assert d3.geo_path(projection).set_digits(6)({"type": "Sphere"}) == "M10,3.141593L0,3.141593L-10,3.141593L-10,-3.141593L-10,-3.141593L0,-3.141593L10,-3.141593L10,3.141593Z"
    assert projection.get_clip_extent() == [[-10, -10], [10, 10]]

def test_transverse_mercator_4():
    projection = d3.geo_transverse_mercator().translate([0, 0]).set_clip_extent([[-10, -10], [10, 10]]).scale(1).set_precision(0)
    assert d3.geo_path(projection).set_digits(6)({"type": "Sphere"}) == "M10,3.141593L0,3.141593L-10,3.141593L-10,-3.141593L-10,-3.141593L0,-3.141593L10,-3.141593L10,3.141593Z"
    assert projection.get_clip_extent() == [[-10, -10], [10, 10]]

def test_transverse_mercator_5():
    projection = d3.geo_transverse_mercator().scale(1).set_clip_extent([[-10, -10], [10, 10]]).translate([0, 0]).set_precision(0)
    assert d3.geo_path(projection).set_digits(6)({"type": "Sphere"}) == "M10,3.141593L0,3.141593L-10,3.141593L-10,-3.141593L-10,-3.141593L0,-3.141593L10,-3.141593L10,3.141593Z"
    assert projection.get_clip_extent() == [[-10, -10], [10, 10]]

def test_transverse_mercator_6():
    projection = d3.geo_transverse_mercator()
    obj = {
        "type": "MultiPoint",
        "coordinates": [
            [-82.35024908550241, 29.649391549778745],
            [-82.35014449996858, 29.65075946917633],
            [-82.34916073446641, 29.65070265688781],
            [-82.3492653331286, 29.64933474064504]
        ]
    }
    projection.fit_extent([[0, 0], [960, 600]], obj)
    assert projection.get_scale() == 15724992.330511674
    assert projection.get_translation() == [20418843.897824816, 21088401.790971387]
    projection.rotate([0, 95]).fit_extent([[0, 0], [960, 600]], obj)
    assert projection.get_scale() == 15724992.330511674
    assert projection.get_translation() == [20418843.897824816, 47161426.43770847]
