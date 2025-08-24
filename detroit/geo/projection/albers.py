from .conic_equal_area import geo_conic_equal_area

def geo_albers():
    return geo_conic_equal_area().parallels([29.5, 45.5]).scale(1070).translate([480, 250]).rotate([96, 0]).set_center([-0.6, 38.7])
