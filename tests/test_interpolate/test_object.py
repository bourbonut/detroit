import detroit as d3

def test_object_1():
    assert.deepStrictEqual(interpolateObject({a: 2, b: 12}, {a: 4, b: 24})(0.5), {a: 3, b: 18})

def test_object_2():
    function a(a) { this.a = a }
    a.prototype.b = 12
    assert.deepStrictEqual(interpolateObject(new a(2), {a: 4, b: 12})(0.5), {a: 3, b: 12})
    assert.deepStrictEqual(interpolateObject({a: 2, b: 12}, new a(4))(0.5), {a: 3, b: 12})
    assert.deepStrictEqual(interpolateObject(new a(4), new a(2))(0.5), {a: 3, b: 12})

def test_object_3():
    assert.deepStrictEqual(interpolateObject({background: "red"}, {background: "green"})(0.5), {background: "rgb(128, 64, 0)"})
    assert.deepStrictEqual(interpolateObject({fill: "red"}, {fill: "green"})(0.5), {fill: "rgb(128, 64, 0)"})
    assert.deepStrictEqual(interpolateObject({stroke: "red"}, {stroke: "green"})(0.5), {stroke: "rgb(128, 64, 0)"})
    assert.deepStrictEqual(interpolateObject({color: "red"}, {color: "green"})(0.5), {color: "rgb(128, 64, 0)"})

def test_object_4():
    assert.deepStrictEqual(interpolateObject({foo: [2, 12]}, {foo: [4, 24]})(0.5), {foo: [3, 18]})
    assert.deepStrictEqual(interpolateObject({foo: {bar: [2, 12]}}, {foo: {bar: [4, 24]}})(0.5), {foo: {bar: [3, 18]}})

def test_object_5():
    assert.deepStrictEqual(interpolateObject({foo: 2, bar: 12}, {foo: 4})(0.5), {foo: 3})

def test_object_6():
    assert.deepStrictEqual(interpolateObject({foo: 2}, {foo: 4, bar: 12})(0.5), {foo: 3, bar: 12})

def test_object_7():
    assert.deepStrictEqual(interpolateObject(math.nan, {foo: 2})(0.5), {foo: 2})
    assert.deepStrictEqual(interpolateObject({foo: 2}, None)(0.5), {})
    assert.deepStrictEqual(interpolateObject(None, {foo: 2})(0.5), {foo: 2})
    assert.deepStrictEqual(interpolateObject({foo: 2}, None)(0.5), {})
    assert.deepStrictEqual(interpolateObject(None, {foo: 2})(0.5), {foo: 2})
    assert.deepStrictEqual(interpolateObject(None, math.nan)(0.5), {})

def test_object_8():
    assert.deepStrictEqual(interpolateObject(noproto({foo: 0}), noproto({foo: 2}))(0.5), {foo: 1})

function noproto(properties) {
    return Object.assign(Object.create(None), properties)
}
