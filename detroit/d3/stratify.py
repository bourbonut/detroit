# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class stratify:
    def __init__(self, content="stratify"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def id(self, id=None):
        """
        Source · If id is specified, sets the id accessor to the given function and returns
        this stratify operator. Otherwise, returns the current id accessor, which defaults to:
        .. code:: javascript

            function id(d) {
              return d.id;
            }

        The id accessor is invoked for each element in the input data passed to the stratify
        operator, being passed the current datum (d) and the current index (i). The returned
        string is then used to identify the node’s relationships in conjunction with the parent
        id. For leaf nodes, the id may be undefined; otherwise, the id must be unique. (Null
        and the empty string are equivalent to undefined.)

        See more informations `here <https://d3js.org/d3-hierarchy/stratify#stratify_id>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (id,))))
        return stratify(content=f"{self.content}.id({arguments})")


    def parentId(self, parentId=None):
        """
        Source · If parentId is specified, sets the parent id accessor to the given function
        and returns this stratify operator. Otherwise, returns the current parent id accessor,
        which defaults to:
        .. code:: javascript

            function parentId(d) {
              return d.parentId;
            }

        The parent id accessor is invoked for each element in the input data passed to the
        stratify operator, being passed the current datum (d) and the current index (i). The
        returned string is then used to identify the node’s relationships in conjunction with
        the id. For the root node, the parent id should be undefined. (Null and the empty
        string are equivalent to undefined.) There must be exactly one root node in the input
        data, and no circular relationships.

        See more informations `here <https://d3js.org/d3-hierarchy/stratify#stratify_parentId>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (parentId,))))
        return stratify(content=f"{self.content}.parentId({arguments})")


    def path(self, path=None):
        """
        Source · If path is specified, sets the path accessor to the given function and returns
        this stratify operator. Otherwise, returns the current path accessor, which defaults to
        undefined.
        If a path accessor is set, the id and parentId accessors are ignored, and a unix-like
        hierarchy is computed on the slash-delimited strings returned by the path accessor,
        imputing parent nodes and ids as necessary.
        For example, given the output of the UNIX find command in the local directory:
        .. code:: javascript

            const paths = [
              "axes.js",
              "channel.js",
              "context.js",
              "legends.js",
              "legends/ramp.js",
              "marks/density.js",
              "marks/dot.js",
              "marks/frame.js",
              "scales/diverging.js",
              "scales/index.js",
              "scales/ordinal.js",
              "stats.js",
              "style.js",
              "transforms/basic.js",
              "transforms/bin.js",
              "transforms/centroid.js",
              "warnings.js",
            ];

        You can say:
        .. code:: javascript

            const root = d3.stratify().path((d) => d)(paths);


        See more informations `here <https://d3js.org/d3-hierarchy/stratify#stratify_path>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (path,))))
        return stratify(content=f"{self.content}.path({arguments})")
