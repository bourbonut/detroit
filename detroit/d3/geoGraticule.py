# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class geoGraticule:
    def __init__(self, content="geoGraticule"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def lines(self):
        """
        Source · Returns an array of GeoJSON LineString geometry objects, one for each meridian
        or parallel for this graticule.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_lines>`_.
        """
        return geoGraticule(content=f"{self.content}.lines()")


    def outline(self):
        """
        Source · Returns a GeoJSON Polygon geometry object representing the outline of this
        graticule, i.e. along the meridians and parallels defining its extent.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_outline>`_.
        """
        return geoGraticule(content=f"{self.content}.outline()")


    def extent(self, extent=None):
        """
        Source · If extent is specified, sets the major and minor extents of this graticule. If
        extent is not specified, returns the current minor extent, which defaults to ⟨⟨-180°,
        -80° - ε⟩, ⟨180°, 80° + ε⟩⟩.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_extent>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (extent,))))
        return geoGraticule(content=f"{self.content}.extent({arguments})")


    def extentMajor(self, extent=None):
        """
        Source · If extent is specified, sets the major extent of this graticule. If extent is
        not specified, returns the current major extent, which defaults to ⟨⟨-180°, -90° + ε⟩,
        ⟨180°, 90° - ε⟩⟩.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_extentMajor>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (extent,))))
        return geoGraticule(content=f"{self.content}.extentMajor({arguments})")


    def extentMinor(self, extent=None):
        """
        Source · If extent is specified, sets the minor extent of this graticule. If extent is
        not specified, returns the current minor extent, which defaults to ⟨⟨-180°, -80° - ε⟩,
        ⟨180°, 80° + ε⟩⟩.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_extentMinor>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (extent,))))
        return geoGraticule(content=f"{self.content}.extentMinor({arguments})")


    def step(self, step=None):
        """
        Source · If step is specified, sets the major and minor step for this graticule. If
        step is not specified, returns the current minor step, which defaults to ⟨10°, 10°⟩.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_step>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (step,))))
        return geoGraticule(content=f"{self.content}.step({arguments})")


    def stepMajor(self, step=None):
        """
        Source · If step is specified, sets the major step for this graticule. If step is not
        specified, returns the current major step, which defaults to ⟨90°, 360°⟩.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_stepMajor>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (step,))))
        return geoGraticule(content=f"{self.content}.stepMajor({arguments})")


    def stepMinor(self, step=None):
        """
        Source · If step is specified, sets the minor step for this graticule. If step is not
        specified, returns the current minor step, which defaults to ⟨10°, 10°⟩.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_stepMinor>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (step,))))
        return geoGraticule(content=f"{self.content}.stepMinor({arguments})")


    def precision(self, angle=None):
        """
        Source · If precision is specified, sets the precision for this graticule, in degrees.
        If precision is not specified, returns the current precision, which defaults to 2.5°.

        See more informations `here <https://d3js.org/d3-geo/shape#graticule_precision>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (angle,))))
        return geoGraticule(content=f"{self.content}.precision({arguments})")
