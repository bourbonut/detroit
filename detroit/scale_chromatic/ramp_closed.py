from ..interpolate import interpolate_rgb_basis_closed
from ..scale import scale_sequential
from .colors import color


def ramp_closed(rang):
    return scale_sequential(interpolate_rgb_basis_closed(colors(rang))).clamp(True)
