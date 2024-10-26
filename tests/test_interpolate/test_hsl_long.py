import detroit as d3
import pytest

def test_hsl_long_1():
    assert interpolateHslLong("steelblue", "brown")(0) == rgb("steelblue") + ""
    assert interpolateHslLong("steelblue", hsl("brown"))(1) == rgb("brown") + ""
    assert interpolateHslLong("steelblue", rgb("brown"))(1) == rgb("brown") + ""

def test_hsl_long_2():
    assert interpolateHslLong("steelblue", "#f00")(0.2) == "rgb(56, 195, 162)"
    assert interpolateHslLong("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2) == "rgba(56, 195, 162, 0.84)"

def test_hsl_long_3():
    i = interpolateHslLong("hsl(10,50%,50%)", "hsl(350,50%,50%)")
    assert i(0.0) == "rgb(191, 85, 64)"
    assert i(0.2) == "rgb(153, 191, 64)"
    assert i(0.4) == "rgb(64, 191, 119)"
    assert i(0.6) == "rgb(64, 119, 191)"
    assert i(0.8) == "rgb(153, 64, 191)"
    assert i(1.0) == "rgb(191, 64, 85)"

def test_hsl_long_4():
    assert interpolateHslLong("#f60", "#000")(0.5) == "rgb(128, 51, 0)"
    assert interpolateHslLong("#6f0", "#fff")(0.5) == "rgb(179, 255, 128)"

def test_hsl_long_5():
    assert interpolateHslLong("#000", "#f60")(0.5) == "rgb(128, 51, 0)"
    assert interpolateHslLong("#fff", "#6f0")(0.5) == "rgb(179, 255, 128)"

def test_hsl_long_6():
    assert interpolateHslLong("#ccc", "#000")(0.5) == "rgb(102, 102, 102)"
    assert interpolateHslLong("#f00", "#000")(0.5) == "rgb(128, 0, 0)"

def test_hsl_long_7():
    assert interpolateHslLong("#000", "#ccc")(0.5) == "rgb(102, 102, 102)"
    assert interpolateHslLong("#000", "#f00")(0.5) == "rgb(128, 0, 0)"

def test_hsl_long_8():
    assert interpolateHslLong(None, hsl(20, 1.0, 0.5))(0.5) == "rgb(255, 85, 0)"

def test_hsl_long_9():
    assert interpolateHslLong(hsl(20, 1.0, 0.5), None)(0.5) == "rgb(255, 85, 0)"
