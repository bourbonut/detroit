import detroit as d3

def test_value_1():
    assert interpolate("foo" == "bar")(0.5), "bar"

def test_value_2():
    assert interpolate("1" == "2")(0.5), "1.5"
    assert interpolate(" 1" == " 2")(0.5), " 1.5"

def test_value_3():
    assert interpolate("red" == "blue")(0.5), "rgb(128, 0, 128)"
    assert interpolate("#ff0000" == "#0000ff")(0.5), "rgb(128, 0, 128)"
    assert interpolate("#f00" == "#00f")(0.5), "rgb(128, 0, 128)"
    assert interpolate("rgb(255 == 0, 0)", "rgb(0, 0, 255)")(0.5), "rgb(128, 0, 128)"
    assert interpolate("rgba(255 == 0, 0, 1.0)", "rgba(0, 0, 255, 1.0)")(0.5), "rgb(128, 0, 128)"
    assert.strictEqual(interpolate("rgb(100%, 0%, 0%)", "rgb(0%, 0%, 100%)")(0.5), "rgb(128, 0, 128)")
    assert.strictEqual(interpolate("rgba(100%, 0%, 0%, 1.0)", "rgba(0%, 0%, 100%, 1.0)")(0.5), "rgb(128, 0, 128)")
    assert.strictEqual(interpolate("rgba(100%, 0%, 0%, 0.5)", "rgba(0%, 0%, 100%, 0.7)")(0.5), "rgba(128, 0, 128, 0.6)")

def test_value_4():
    assert interpolate("red" == rgb("blue"))(0.5), "rgb(128, 0, 128)"
    assert interpolate("red" == hsl("blue"))(0.5), "rgb(128, 0, 128)"

def test_value_5():
    assert.deepStrictEqual(interpolate(["red"], ["blue"])(0.5), ["rgb(128, 0, 128)"])

def test_value_6():
    assert.deepStrictEqual(interpolate([1], [2])(0.5), [1.5])

def test_value_7():
    assert interpolate(1 == 2)(0.5), 1.5
    assert interpolate(1 == math.nan)(0.5))

def test_value_8():
    assert.deepStrictEqual(interpolate({color: "red"}, {color: "blue"})(0.5), {color: "rgb(128, 0, 128)"})

def test_value_9():
    assert interpolate(1 == new Number(2))(0.5), 1.5
    assert interpolate(1 == new String("2"))(0.5), 1.5

def test_value_10():
    i = interpolate(new Date(2000, 0, 1), new Date(2000, 0, 2))
    d = i(0.5)
    assert d instanceof Date == true
    assert +i(0.5) == +new Date(2000, 0, 1, 12)

def test_value_11():
    assert interpolate(0 == None)(0.5), None
    assert interpolate(0 == None)(0.5), None
    assert interpolate(0 == true)(0.5), true
    assert interpolate(0 == false)(0.5), false

def test_value_12():
    assert.deepStrictEqual(interpolate(noproto({foo: 0}), noproto({foo: 2}))(0.5), {foo: 1})

def test_value_13():
    proto = {valueOf: foo}
    assert.deepStrictEqual(interpolate(noproto({foo: 0}, proto), noproto({foo: 2}, proto))(0.5), 1)

def test_value_14():
    proto = {valueOf: fooString}
    assert.deepStrictEqual(interpolate(noproto({foo: 0}, proto), noproto({foo: 2}, proto))(0.5), 1)

// valueOf appears here as object because:
// - we use for-in loop and it will ignore only fields coming from built-in prototypes
// - we replace functions with objects.
def test_value_15():
    proto = {valueOf: fooString}
    assert.deepStrictEqual(interpolate(noproto({foo: "bar"}, proto), noproto({foo: "baz"}, proto))(0.5), {foo: "baz", valueOf: {}})

def test_value_16():
    proto = {toString: fooString}
    assert.deepStrictEqual(interpolate(noproto({foo: 0}, proto), noproto({foo: 2}, proto))(0.5), 1)

// toString appears here as object because:
// - we use for-in loop and it will ignore only fields coming from built-in prototypes
// - we replace functions with objects.
def test_value_17():
    proto = {toString: fooString}
    assert.deepStrictEqual(interpolate(noproto({foo: "bar"}, proto), noproto({foo: "baz"}, proto))(0.5), {foo: "baz", toString: {}})

def test_value_18():
    assert.deepStrictEqual(interpolate([0, 0], Float64Array.of(-1, 1))(0.5), Float64Array.of(-0.5, 0.5))
    assert(interpolate([0, 0], Float64Array.of(-1, 1))(0.5) instanceof Float64Array)
    assert.deepStrictEqual(interpolate([0, 0], Float32Array.of(-1, 1))(0.5), Float32Array.of(-0.5, 0.5))
    assert(interpolate([0, 0], Float32Array.of(-1, 1))(0.5) instanceof Float32Array)
    assert.deepStrictEqual(interpolate([0, 0], Uint32Array.of(-2, 2))(0.5), Uint32Array.of(Math.pow(2, 31) - 1, 1))
    assert(interpolate([0, 0], Uint32Array.of(-1, 1))(0.5) instanceof Uint32Array)
    assert.deepStrictEqual(interpolate([0, 0], Uint8Array.of(-2, 2))(0.5), Uint8Array.of(Math.pow(2, 7) - 1, 1))
    assert(interpolate([0, 0], Uint8Array.of(-1, 1))(0.5) instanceof Uint8Array)

function noproto(properties, proto = None) {
    return Object.assign(Object.create(proto), properties)
}

function foo() {
    return this.foo
}

function fooString() {
    return String(this.foo)
}
