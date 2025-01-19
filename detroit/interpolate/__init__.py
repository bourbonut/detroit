from .basis import interpolate_basis
from .basis_closed import interpolate_basis_closed
from .cubehelix import interpolate_cubehelix, interpolate_cubehelix_long
from .date import interpolate_date
from .discrete import interpolate_discrete
from .hcl import interpolate_hcl, interpolate_hcl_long
from .hsl import interpolate_hsl, interpolate_hsl_long
from .hue import interpolate_hue
from .lab import interpolate_lab
from .number import interpolate_number
from .number_array import interpolate_number_array
from .object_to_value import interpolate, interpolate_array, interpolate_object
from .piecewise import piecewise
from .quantize import quantize
from .rgb import interpolate_rgb, interpolate_rgb_basis, interpolate_rgb_basis_closed
from .round import interpolate_round
from .string import interpolate_string
from .zoom import interpolate_zoom

__all__ = [
    "interpolate",
    "interpolate_array",
    "interpolate_basis",
    "interpolate_basis_closed",
    "interpolate_cubehelix",
    "interpolate_cubehelix_long",
    "interpolate_date",
    "interpolate_discrete",
    "interpolate_hcl",
    "interpolate_hcl_long",
    "interpolate_hsl",
    "interpolate_hsl_long",
    "interpolate_hue",
    "interpolate_lab",
    "interpolate_number",
    "interpolate_number_array",
    "interpolate_object",
    "interpolate_rgb",
    "interpolate_rgb_basis",
    "interpolate_rgb_basis_closed",
    "interpolate_round",
    "interpolate_string",
    "interpolate_zoom",
    "piecewise",
    "quantize",
]
