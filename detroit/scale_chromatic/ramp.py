from ..interpolate import interpolate_rgb_basis


def ramp(scheme):
    return interpolate_rgb_basis(scheme[-1])
