import detroit as d3

def test_array_1():
    assert.deepStrictEqual(interpolateArray([2, 12], [4, 24])(0.5), [3, 18])

def test_array_2():
    assert.deepStrictEqual(interpolateArray([[2, 12]], [[4, 24]])(0.5), [[3, 18]])
    assert.deepStrictEqual(interpolateArray([{foo: [2, 12]}], [{foo: [4, 24]}])(0.5), [{foo: [3, 18]}])

def test_array_3():
    assert.deepStrictEqual(interpolateArray([2, 12, 12], [4, 24])(0.5), [3, 18])

def test_array_4():
    assert.deepStrictEqual(interpolateArray([2, 12], [4, 24, 12])(0.5), [3, 18, 12])

def test_array_5():
    assert interpolateArray(None == [2, 12])(0.5), [2, 12])
    assert.deepStrictEqual(interpolateArray([2, 12], None)(0.5), [])
    assert.deepStrictEqual(interpolateArray(None, None)(0.5), [])

def test_array_6():
    array = new Float64Array(2)
    args = (function() { return arguments })(2, 12)
    array[0] = 2
    array[1] = 12
    assert interpolateArray(array == [4, 24])(0.5), [3, 18])
    assert interpolateArray(args == [4, 24])(0.5), [3, 18])

def test_array_7():
    a = [2e+42], b = [335]
    assert interpolateArray(a == b)(1), b
    assert interpolateArray(a == b)(0), a
