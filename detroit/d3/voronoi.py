# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class voronoi:
    def __init__(self, content="voronoi"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def delaunay(self):
        """
        The Voronoi diagram’s associated Delaunay triangulation.
        The circumcenters of the Delaunay triangles as a Float64Array [cx0, cy0, cx1, cy1, …].
        Each contiguous pair of coordinates cx, cy is the circumcenter for the corresponding
        triangle. These circumcenters form the coordinates of the Voronoi cell polygons.
        A Float64Array [vx0, vy0, wx0, wy0, …] where each non-zero quadruple describes an open
        (infinite) cell on the outer hull, giving the directions of two open half-lines.
        The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram.
        These values only affect the rendering methods (voronoi.render, voronoi.renderBounds,
        voronoi.renderCell).

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_delaunay>`_.
        """
        return voronoi(content=f"{self.content}.delaunay()")


    def circumcenters(self):
        """
        The circumcenters of the Delaunay triangles as a Float64Array [cx0, cy0, cx1, cy1, …].
        Each contiguous pair of coordinates cx, cy is the circumcenter for the corresponding
        triangle. These circumcenters form the coordinates of the Voronoi cell polygons.
        A Float64Array [vx0, vy0, wx0, wy0, …] where each non-zero quadruple describes an open
        (infinite) cell on the outer hull, giving the directions of two open half-lines.
        The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram.
        These values only affect the rendering methods (voronoi.render, voronoi.renderBounds,
        voronoi.renderCell).

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_circumcenters>`_.
        """
        return voronoi(content=f"{self.content}.circumcenters()")


    def vectors(self):
        """
        A Float64Array [vx0, vy0, wx0, wy0, …] where each non-zero quadruple describes an open
        (infinite) cell on the outer hull, giving the directions of two open half-lines.
        The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram.
        These values only affect the rendering methods (voronoi.render, voronoi.renderBounds,
        voronoi.renderCell).

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_vectors>`_.
        """
        return voronoi(content=f"{self.content}.vectors()")


    def xmin(self):
        """
        The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram.
        These values only affect the rendering methods (voronoi.render, voronoi.renderBounds,
        voronoi.renderCell).

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_bounds>`_.
        """
        return voronoi(content=f"{self.content}.xmin()")


    def ymin(self):
        """
        The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram.
        These values only affect the rendering methods (voronoi.render, voronoi.renderBounds,
        voronoi.renderCell).

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_bounds>`_.
        """
        return voronoi(content=f"{self.content}.ymin()")


    def xmax(self):
        """
        The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram.
        These values only affect the rendering methods (voronoi.render, voronoi.renderBounds,
        voronoi.renderCell).

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_bounds>`_.
        """
        return voronoi(content=f"{self.content}.xmax()")


    def ymax(self):
        """
        The bounds of the viewport [xmin, ymin, xmax, ymax] for rendering the Voronoi diagram.
        These values only affect the rendering methods (voronoi.render, voronoi.renderBounds,
        voronoi.renderCell).

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_bounds>`_.
        """
        return voronoi(content=f"{self.content}.ymax()")


    def contains(self, i=None, x=None, y=None):
        """
        Source · Returns true if the cell with the specified index i contains the specified
        point ⟨x, y⟩; i.e., whether the point i is the closest point in the diagram to the
        specified point. (This method is not affected by the associated Voronoi diagram’s
        viewport bounds.)

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_contains>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (i, x, y))))
        return voronoi(content=f"{self.content}.contains({arguments})")


    def neighbors(self, i=None):
        """
        .. code:: javascript

            voronoi.neighbors(-1) // []

        Source · Returns an iterable over the indexes of the cells that share a common edge
        with the specified cell i. Voronoi neighbors are always neighbors on the Delaunay
        graph, but the converse is false when the common edge has been clipped out by the
        Voronoi diagram’s viewport.

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_neighbors>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (i,))))
        return voronoi(content=f"{self.content}.neighbors({arguments})")


    def render(self, context=None):
        """
        Source · Renders the mesh of Voronoi cells to the specified context. The specified
        context must implement the context.moveTo and context.lineTo methods from the
        CanvasPathMethods API. If a context is not specified, an SVG path string is returned
        instead.

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_render>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (context,))))
        return voronoi(content=f"{self.content}.render({arguments})")


    def renderBounds(self, context=None):
        """
        Source · Renders the viewport extent to the specified context. The specified context
        must implement the context.rect method from the CanvasPathMethods API. Equivalent to
        context.rect(voronoi.xmin, voronoi.ymin, voronoi.xmax - voronoi.xmin, voronoi.ymax -
        voronoi.ymin). If a context is not specified, an SVG path string is returned instead.

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_renderBounds>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (context,))))
        return voronoi(content=f"{self.content}.renderBounds({arguments})")


    def renderCell(self, i=None, context=None):
        """
        Source · Renders the cell with the specified index i to the specified context. The
        specified context must implement the context.moveTo , context.lineTo and
        context.closePath methods from the CanvasPathMethods API. If a context is not
        specified, an SVG path string is returned instead.

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_renderCell>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (i, context))))
        return voronoi(content=f"{self.content}.renderCell({arguments})")


    def cellPolygons(self):
        """
        Source · Returns an iterable over the non-empty polygons for each cell, with the cell
        index as property. See also voronoi.renderCell.

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_cellPolygons>`_.
        """
        return voronoi(content=f"{self.content}.cellPolygons()")


    def cellPolygon(self, i=None):
        """
        Source · Returns the convex, closed polygon [[x0, y0], [x1, y1], …, [x0, y0]]
        representing the cell for the specified point i. See also voronoi.renderCell.

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_cellPolygon>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (i,))))
        return voronoi(content=f"{self.content}.cellPolygon({arguments})")


    def update(self):
        """
        Source · Updates the Voronoi diagram and underlying triangulation after the points have
        been modified in-place — useful for Lloyd’s relaxation. Calls delaunay.update on the
        underlying Delaunay triangulation.

        See more informations `here <https://d3js.org/d3-delaunay/voronoi#voronoi_update>`_.
        """
        return voronoi(content=f"{self.content}.update()")
