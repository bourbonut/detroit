# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class geoPath:
    def __init__(self, content="geoPath"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def area(self, object=None):
        """
        Source · Returns the projected planar area (typically in square pixels) for the
        specified GeoJSON object.
        .. code:: javascript

            path.area(california) // 17063.1671837991 px²

        Point, MultiPoint, LineString and MultiLineString geometries have zero area. For
        Polygon and MultiPolygon geometries, this method first computes the area of the
        exterior ring, and then subtracts the area of any interior holes. This method observes
        any clipping performed by the projection; see projection.clipAngle and
        projection.clipExtent. This is the planar equivalent of geoArea.

        See more informations `here <https://d3js.org/d3-geo/path#path_area>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (object,))))
        return geoPath(content=f"{self.content}.area({arguments})")


    def bounds(self, object=None):
        """
        Source · Returns the projected planar bounding box (typically in pixels) for the
        specified GeoJSON object.
        .. code:: javascript

            path.bounds(california) // [[18.48513821663947, 159.95146883594333], [162.7651668852596, 407.09641570706725]]

        The bounding box is represented by a two-dimensional array: [[x₀, y₀], [x₁, y₁]], where
        x₀ is the minimum x-coordinate, y₀ is the minimum y coordinate, x₁ is maximum
        x-coordinate, and y₁ is the maximum y coordinate. This is handy for, say, zooming in to
        a particular feature. (Note that in projected planar coordinates, the minimum latitude
        is typically the maximum y-value, and the maximum latitude is typically the minimum
        y-value.) This method observes any clipping performed by the projection; see
        projection.clipAngle and projection.clipExtent. This is the planar equivalent of
        geoBounds.

        See more informations `here <https://d3js.org/d3-geo/path#path_bounds>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (object,))))
        return geoPath(content=f"{self.content}.bounds({arguments})")


    def centroid(self, object=None):
        """
        Source · Returns the projected planar centroid (typically in pixels) for the specified
        GeoJSON object.
        .. code:: javascript

            path.centroid(california) // [82.08679434495191, 288.14204870673404]

        This is handy for, say, labeling state or county boundaries, or displaying a symbol
        map. For example, a noncontiguous cartogram might scale each state around its centroid.
        This method observes any clipping performed by the projection; see projection.clipAngle
        and projection.clipExtent. This is the planar equivalent of geoCentroid.

        See more informations `here <https://d3js.org/d3-geo/path#path_centroid>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (object,))))
        return geoPath(content=f"{self.content}.centroid({arguments})")


    def digits(self, digits=None):
        """
        Source · If digits is specified (as a non-negative number), sets the number of
        fractional digits for coordinates generated in SVG path strings.
        .. code:: javascript

            const path = d3.geoPath().digits(3);

        If projection is not specified, returns the current number of digits, which defaults to
        3.
        .. code:: javascript

            path.digits() // 3

        This option only applies when the associated context is null, as when this arc
        generator is used to produce path data.

        See more informations `here <https://d3js.org/d3-geo/path#path_digits>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (digits,))))
        return geoPath(content=f"{self.content}.digits({arguments})")


    def measure(self, object=None):
        """
        Source · Returns the projected planar length (typically in pixels) for the specified
        GeoJSON object.
        .. code:: javascript

            path.measure(california) // 825.7124297512761

        Point and MultiPoint geometries have zero length. For Polygon and MultiPolygon
        geometries, this method computes the summed length of all rings. This method observes
        any clipping performed by the projection; see projection.clipAngle and
        projection.clipExtent. This is the planar equivalent of geoLength.

        See more informations `here <https://d3js.org/d3-geo/path#path_measure>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (object,))))
        return geoPath(content=f"{self.content}.measure({arguments})")


    def projection(self, projection=None):
        """
        Source · If a projection is specified, sets the current projection to the specified
        projection.
        .. code:: javascript

            const path = d3.geoPath().projection(d3.geoAlbers());

        If projection is not specified, returns the current projection.
        .. code:: javascript

            path.projection() // a d3.geoAlbers instance

        The projection defaults to null, which represents the identity transformation: the
        input geometry is not projected and is instead rendered directly in raw coordinates.
        This can be useful for fast rendering of pre-projected geometry, or for fast rendering
        of the equirectangular projection.
        The given projection is typically one of D3’s built-in geographic projections; however,
        any object that exposes a projection.stream function can be used, enabling the use of
        custom projections. See D3’s transforms for more examples of arbitrary geometric
        transformations.

        See more informations `here <https://d3js.org/d3-geo/path#path_projection>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (projection,))))
        return geoPath(content=f"{self.content}.projection({arguments})")


    def context(self, context=None):
        """
        Source · If context is specified, sets the current render context and returns the path
        generator.
        .. code:: javascript

            const context = canvas.getContext("2d");
            const path = d3.geoPath().context(context);

        If the context is null, then the path generator will return an SVG path string; if the
        context is non-null, the path generator will instead call methods on the specified
        context to render geometry. The context must implement the following subset of the
        CanvasRenderingContext2D API:
        If a context is not specified, returns the current render context which defaults to
        null. See also d3-path.

        See more informations `here <https://d3js.org/d3-geo/path#path_context>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (context,))))
        return geoPath(content=f"{self.content}.context({arguments})")


    def pointRadius(self, radius=None):
        """
        Source · If radius is specified, sets the radius used to display Point and MultiPoint
        geometries to the specified number.
        .. code:: javascript

            const path = d3.geoPath().pointRadius(10);

        If radius is not specified, returns the current radius accessor.
        .. code:: javascript

            path.pointRadius() // 10

        The radius accessor defaults to 4.5. While the radius is commonly specified as a number
        constant, it may also be specified as a function which is computed per feature, being
        passed the any arguments passed to the path generator. For example, if your GeoJSON
        data has additional properties, you might access those properties inside the radius
        function to vary the point size; alternatively, you could symbol and a projection for
        greater flexibility.

        See more informations `here <https://d3js.org/d3-geo/path#path_pointRadius>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (radius,))))
        return geoPath(content=f"{self.content}.pointRadius({arguments})")
