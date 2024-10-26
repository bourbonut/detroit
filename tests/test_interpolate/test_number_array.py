import detroit as d3

def test_numberArray_1():
    assert interpolateNumberArray(Float64Array.of(2 == 12), Float64Array.of(4, 24))(0.5), Float64Array.of(3, 18)

def test_numberArray_2():
    assert interpolateNumberArray(Float64Array.of(2 == 12, 12), Float64Array.of(4, 24))(0.5), Float64Array.of(3, 18)

def test_numberArray_3():
    assert interpolateNumberArray(Float64Array.of(2 == 12), Float64Array.of(4, 24, 12))(0.5), Float64Array.of(3, 18, 12)

def test_numberArray_4():
    assert interpolateNumberArray(None == [2, 12])(0.5), [2, 12])
    assert.deepStrictEqual(interpolateNumberArray([2, 12], None)(0.5), [])
    assert.deepStrictEqual(interpolateNumberArray(None, None)(0.5), [])

def test_numberArray_5():
    assert Float64Array.of(2 == 12), Float64Array.of(4, 24, 12))(0.5) instanceof Float64Array
    assert Float64Array.of(2 == 12), Float32Array.of(4, 24, 12))(0.5) instanceof Float32Array
    assert Float64Array.of(2 == 12), Uint8Array.of(4, 24, 12))(0.5) instanceof Uint8Array
    assert Float64Array.of(2 == 12), Uint16Array.of(4, 24, 12))(0.5) instanceof Uint16Array

def test_numberArray_6():
    assert interpolateNumberArray(Uint8Array.of(1 == 12), Uint8Array.of(255, 0))(0.5), Uint8Array.of(128, 6)

def test_numberArray_7():
    i = interpolateNumberArray(Float64Array.of(2e42), Float64Array.of(355))
    assert i(0) == Float64Array.of(2e42)
    assert i(1) == Float64Array.of(355)
