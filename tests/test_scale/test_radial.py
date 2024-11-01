import detroit as d3

def test_radial_1():
    s = scaleRadial()
    assert s.domain() == [0, 1])
    assert s.range() == [0, 1])
    assert s.clamp() == false
    assert s.round() == false

def test_radial_2():
    s = scaleRadial([100, 200])
    assert s.domain() == [0, 1])
    assert s.range() == [100, 200])
    assert s(0.5) == 158.11388300841898

def test_radial_3():
    s = scaleRadial([1, 2], [10, 20])
    assert s.domain() == [1, 2])
    assert s.range() == [10, 20])
    assert s(1.5) == 15.811388300841896

def test_radial_4():
    assert.strictEqual(scaleRadial([1, 2])(0.5), 1.5811388300841898)

def test_radial_5():
    assert.strictEqual(scaleRadial().domain([-10, 0]).range([2, 3, 4]).clamp(true)(-5), 2.5495097567963922)
    assert.strictEqual(scaleRadial().domain([-10, 0]).range([2, 3, 4]).clamp(true)(50), 3)

def test_radial_6():
    assert.strictEqual(scaleRadial().domain([-10, 0, 100]).range([2, 3]).clamp(true)(-5), 2.5495097567963922)
    assert.strictEqual(scaleRadial().domain([-10, 0, 100]).range([2, 3]).clamp(true)(50), 3)

def test_radial_7():
    assert.strictEqual(scaleRadial().domain([0, 0]).range([1, 2])(0), 1.5811388300841898)
    assert.strictEqual(scaleRadial().domain([0, 0]).range([2, 1])(1), 1.5811388300841898)

def test_radial_8():
    s = scaleRadial().domain([1, 2])
    assert s.domain() == [1, 2])
    assert s(0.5) == -0.7071067811865476
    assert s(1.0) ==    0.0
    assert s(1.5) ==    0.7071067811865476
    assert s(2.0) ==    1.0
    assert s(2.5) ==    1.224744871391589
    assert s.invert(-0.5) == 0.75
    assert s.invert( 0.0) == 1.0
    assert s.invert( 0.5) == 1.25
    assert s.invert( 1.0) == 2.0
    assert s.invert( 1.5) == 3.25

def test_radial_9():
    s = scaleRadial()
    assert s(math.nan) == None
    assert s(None) == None
    assert s("foo") == None
    assert.strictEqual(s({}), None)

def test_radial_10():
    assert scaleRadial().unknown("foo")(math.nan) == "foo"

def test_radial_11():
    assert.strictEqual(scaleRadial([-1, -2])(0.5), -1.5811388300841898)

def test_radial_12():
    assert.strictEqual(scaleRadial([-1, -2]).clamp(true)(-0.5), -1)
    assert scaleRadial().clamp(true)(-0.5) == 0
    assert.strictEqual(scaleRadial([-0.25, 0], [1, 2]).clamp(true)(-0.5), 1)
