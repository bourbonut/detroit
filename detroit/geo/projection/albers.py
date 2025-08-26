from ..common import Projection
from .conic_equal_area import geo_conic_equal_area


def geo_albers() -> Projection:
    """
    The Albers' equal area-conic projection. This is a U.S.-centric
    configuration of :func:`d3.geo_conic_equal_area <geo_conic_equal_area>`.

    Returns
    -------
    Projection
        Projection object
    """
    return (
        geo_conic_equal_area()
        .parallels([29.5, 45.5])
        .scale(1070)
        .translate([480, 250])
        .rotate([96, 0])
        .set_center([-0.6, 38.7])
    )
