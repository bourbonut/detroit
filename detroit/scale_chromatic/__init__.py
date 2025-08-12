from .categorical.accent import SCHEME_ACCENT
from .categorical.category10 import SCHEME_CATEGORY_10
from .categorical.dark2 import SCHEME_DARK_2
from .categorical.observable10 import SCHEME_OBSERVABLE_10
from .categorical.paired import SCHEME_PAIRED
from .categorical.pastel1 import SCHEME_PASTEL_1
from .categorical.pastel2 import SCHEME_PASTEL_2
from .categorical.set1 import SCHEME_SET_1
from .categorical.set2 import SCHEME_SET_2
from .categorical.set3 import SCHEME_SET_3
from .categorical.tableau10 import SCHEME_TABLEAU_10
from .diverging.br_bg import SCHEME_BRBG, interpolate_brbg
from .diverging.pi_yg import SCHEME_PIYG, interpolate_piyg
from .diverging.pr_gn import SCHEME_PRGN, interpolate_prgn
from .diverging.pu_or import SCHEME_PUOR, interpolate_puor
from .diverging.rd_bu import SCHEME_RDBU, interpolate_rdbu
from .diverging.rd_gy import SCHEME_RDGY, interpolate_rdgy
from .diverging.rd_yl_bu import SCHEME_RDYLBU, interpolate_rdylbu
from .diverging.rd_yl_gn import SCHEME_RDYLGN, interpolate_rdylgn
from .diverging.spectral import SCHEME_SPECTRAL, interpolate_spectral
from .sequential_multi.bu_gn import SCHEME_BUGN, interpolate_bugn
from .sequential_multi.bu_pu import SCHEME_BUPU, interpolate_bupu
from .sequential_multi.cividis import interpolate_cividis
from .sequential_multi.cubehelix import interpolate_cubehelix_default
from .sequential_multi.gn_bu import SCHEME_GNBU, interpolate_gnbu
from .sequential_multi.or_rd import SCHEME_ORRD, interpolate_orrd
from .sequential_multi.pu_bu import SCHEME_PUBU, interpolate_pubu
from .sequential_multi.pu_bu_gn import SCHEME_PUBUGN, interpolate_pubugn
from .sequential_multi.pu_rd import SCHEME_PURD, interpolate_purd
from .sequential_multi.rainbow import (
    interpolate_cool,
    interpolate_rainbow,
    interpolate_warm,
)
from .sequential_multi.rd_pu import SCHEME_RDPU, interpolate_rdpu
from .sequential_multi.sinebow import interpolate_sinebow
from .sequential_multi.turbo import interpolate_turbo
from .sequential_multi.viridis import (
    interpolate_inferno,
    interpolate_magma,
    interpolate_plasma,
    interpolate_viridis,
)
from .sequential_multi.yl_gn import SCHEME_YLGN, interpolate_ylgn
from .sequential_multi.yl_gn_bu import SCHEME_YLGNBU, interpolate_ylgnbu
from .sequential_multi.yl_or_br import SCHEME_YLORBR, interpolate_ylorbr
from .sequential_multi.yl_or_rd import SCHEME_YLORRD, interpolate_ylorrd
from .sequential_single.blues import SCHEME_BLUES, interpolate_blues
from .sequential_single.greens import SCHEME_GREENS, interpolate_greens
from .sequential_single.greys import SCHEME_GREYS, interpolate_greys
from .sequential_single.oranges import SCHEME_ORANGES, interpolate_oranges
from .sequential_single.purples import SCHEME_PURPLES, interpolate_purples
from .sequential_single.reds import SCHEME_REDS, interpolate_reds

__all__ = [
    "SCHEME_ACCENT",
    "SCHEME_BLUES",
    "SCHEME_BRBG",
    "SCHEME_BUGN",
    "SCHEME_BUPU",
    "SCHEME_CATEGORY_10",
    "SCHEME_DARK_2",
    "SCHEME_GNBU",
    "SCHEME_GREENS",
    "SCHEME_GREYS",
    "SCHEME_OBSERVABLE_10",
    "SCHEME_ORANGES",
    "SCHEME_ORRD",
    "SCHEME_PAIRED",
    "SCHEME_PASTEL_1",
    "SCHEME_PASTEL_2",
    "SCHEME_PIYG",
    "SCHEME_PRGN",
    "SCHEME_PUBU",
    "SCHEME_PUBUGN",
    "SCHEME_PUOR",
    "SCHEME_PURD",
    "SCHEME_PURPLES",
    "SCHEME_RDBU",
    "SCHEME_RDGY",
    "SCHEME_RDPU",
    "SCHEME_RDYLBU",
    "SCHEME_RDYLGN",
    "SCHEME_REDS",
    "SCHEME_SET_1",
    "SCHEME_SET_2",
    "SCHEME_SET_3",
    "SCHEME_SPECTRAL",
    "SCHEME_TABLEAU_10",
    "SCHEME_YLGN",
    "SCHEME_YLGNBU",
    "SCHEME_YLORBR",
    "SCHEME_YLORRD",
    "interpolate_blues",
    "interpolate_brbg",
    "interpolate_bugn",
    "interpolate_bupu",
    "interpolate_cividis",
    "interpolate_cool",
    "interpolate_cubehelix_default",
    "interpolate_gnbu",
    "interpolate_greens",
    "interpolate_greys",
    "interpolate_inferno",
    "interpolate_magma",
    "interpolate_oranges",
    "interpolate_orrd",
    "interpolate_piyg",
    "interpolate_plasma",
    "interpolate_prgn",
    "interpolate_pubu",
    "interpolate_pubugn",
    "interpolate_puor",
    "interpolate_purd",
    "interpolate_purples",
    "interpolate_rainbow",
    "interpolate_rdbu",
    "interpolate_rdgy",
    "interpolate_rdpu",
    "interpolate_rdylbu",
    "interpolate_rdylgn",
    "interpolate_reds",
    "interpolate_sinebow",
    "interpolate_spectral",
    "interpolate_turbo",
    "interpolate_viridis",
    "interpolate_warm",
    "interpolate_ylgn",
    "interpolate_ylgnbu",
    "interpolate_ylorbr",
    "interpolate_ylorrd",
]
