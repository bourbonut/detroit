from ..interpolate import interpolate_rgb_basis_closed
from ..scale import scale_sequential
from .colors import colors


def ramp_closed(range_values):
    return scale_sequential(interpolate_rgb_basis_closed(colors(range_values))).clamp(
        True
    )
