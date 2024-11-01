import detroit as d3

def test_hsl_long_1():
    assert d3.interpolate_hsl_long("steelblue", "brown")(0) == str(d3.rgb("steelblue"))
    assert d3.interpolate_hsl_long("steelblue", d3.hsl("brown"))(1) == str(d3.rgb("brown"))
    assert d3.interpolate_hsl_long("steelblue", d3.rgb("brown"))(1) == str(d3.rgb("brown"))

def test_hsl_long_2():
    assert d3.interpolate_hsl_long("steelblue", "#f00")(0.2) == "rgb(56, 195, 162)"
    assert d3.interpolate_hsl_long("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2) == "rgba(56, 195, 162, 0.84)"

def test_hsl_long_3():
    i = d3.interpolate_hsl_long("hsl(10,50%,50%)", "hsl(350,50%,50%)")
    assert i(0.0) == "rgb(191, 85, 64)"
    assert i(0.2) == "rgb(153, 191, 64)"
    assert i(0.4) == "rgb(64, 191, 119)"
    assert i(0.6) == "rgb(64, 119, 191)"
    assert i(0.8) == "rgb(153, 64, 191)"
    assert i(1.0) == "rgb(191, 64, 85)"

def test_hsl_long_4():
    assert d3.interpolate_hsl_long("#f60", "#000")(0.5) == "rgb(128, 51, 0)"
    assert d3.interpolate_hsl_long("#6f0", "#fff")(0.5) == "rgb(178, 255, 128)" # 179

def test_hsl_long_5():
    assert d3.interpolate_hsl_long("#000", "#f60")(0.5) == "rgb(128, 51, 0)"
    assert d3.interpolate_hsl_long("#fff", "#6f0")(0.5) == "rgb(178, 255, 128)" # 179

def test_hsl_long_6():
    assert d3.interpolate_hsl_long("#ccc", "#000")(0.5) == "rgb(102, 102, 102)"
    assert d3.interpolate_hsl_long("#f00", "#000")(0.5) == "rgb(128, 0, 0)"

def test_hsl_long_7():
    assert d3.interpolate_hsl_long("#000", "#ccc")(0.5) == "rgb(102, 102, 102)"
    assert d3.interpolate_hsl_long("#000", "#f00")(0.5) == "rgb(128, 0, 0)"
