from ...color import cubehelix
from ...interpolate import interpolate_cubehelix_long

interpolate_cubehelix_default = interpolate_cubehelix_long(
    cubehelix(300, 0.5, 0.0), cubehelix(-240, 0.5, 1.0)
)
