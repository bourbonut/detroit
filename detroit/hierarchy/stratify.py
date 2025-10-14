from collections.abc import Callable
from typing import Any, TypeVar

from ..array import argpass
from .accessors import optional
from .hierarchy import Node, compute_height

TStratify = TypeVar("Stratify", bound="Stratify")


class SparseNode:
    def __init__(self):
        self.depth = -1
        self.height = 0
        self.parent = None


preroot = SparseNode()
ambiguous = {}
imputed = {}


@argpass
def default_id(d: dict[str, Any]) -> Any | None:
    return d.get("id")


@argpass
def default_parent_id(d: dict[str, Any]) -> Any | None:
    return d.get("parent_id")


class Stratify:
    """
    Stratify operator
    """
    def __init__(self):
        self._id = default_id
        self._parent_id = default_parent_id
        self._path = None

    def __call__(self, data: list[dict[str, Any]]) -> Node:
        """
        Generates a new hierarchy from the specified tabular data.

        Parameters
        ----------
        data : list[dict[str, Any]]
            Data

        Returns
        -------
        Node
            Node object
        """
        nodes = list(data)
        current_id = self._id
        current_parent_id = self._parent_id
        node_by_key = {}
        root = None

        if self._path is not None:
            norms = [normalize(self._path(d, i, data)) for i, d in enumerate(nodes)]
            parents = [parent_of(x) for x in norms]
            set_norms = set(norms)
            set_norms.add("")
            for i in parents:
                if i not in set_norms:
                    set_norms.add(i)
                    norms.append(i)
                    parents.append(parent_of(i))
                    nodes.append(imputed)

            @argpass
            def current_id(_, i):
                return norms[i]

            @argpass
            def current_parent_id(_, i):
                return parents[i]

        n = len(nodes)
        for i, d in enumerate(nodes):
            node = nodes[i] = Node(d)

            node_id = current_id(d, i, data)
            if node_id is not None:
                node_id = str(node_id)
                if node_id != "":
                    node_key = node.id = node_id
                    node_by_key[node_key] = (
                        ambiguous if node_key in node_by_key else node
                    )

            node_id = current_parent_id(d, i, data)
            if node_id is not None:
                node_id = str(node_id)
                if node_id != "":
                    node.parent = node_id

        for node in nodes:
            node_id = node.parent
            if node_id:
                parent = node_by_key.get(node_id)
                if parent == ambiguous:
                    raise ValueError("Ambiguous")
                if parent is None:
                    raise ValueError(f"Missing: {node_id!r}")
                if parent.children:
                    parent.children.append(node)
                else:
                    parent.children = [node]
                node.parent = parent
            else:
                if root is not None:
                    raise RuntimeError("Multiple roots")
                root = node

        if root is None:
            raise RuntimeError("No root")

        if self._path is not None:
            while root.data == imputed and len(root.children) == 1:
                root = root.children[0]
                n -= 1
            for node in nodes:
                if node.data != imputed:
                    break
                node.data = None

        root.parent = preroot

        def update(node):
            nonlocal n
            node.depth = node.parent.depth + 1
            n -= 1

        root.each_before(update).each_before(compute_height)
        root.parent = None
        if n > 0:
            raise RuntimeError("Cycle")
        return root

    def set_id(
        self, id_func: Callable[[Node, int, list[dict[str, Any]]], str]
    ) -> TStratify:
        """
        Sets the id accessor to the given function and returns this stratify
        operator.

        Parameters
        ----------
        id_func : Callable[[Node, int, list[dict[str, Any]]], str]
            Function to call which takes as argument:

            * **node** (:code:`Node`) - the descendant node
            * **i** (:code:`int`) - the index of the descendant node
            * **data** (:code:`list[dict[str, Any]]`) - Data

            It should return an ID for the node's relationships in the
            conjuction with the parent ID.

        Returns
        -------
        Stratify
            Itself
        """
        self._id = argpass(optional(id_func))
        return self

    def set_parent_id(
        self, parent_id: Callable[[Node, int, list[dict[str, Any]]], str]
    ) -> TStratify:
        """
        Sets the parent id accessor to the given function and returns this
        stratify operator.

        Parameters
        ----------
        parent_id : Callable[[Node, int, list[dict[str, Any]]], str]
            Function to call which takes as argument:

            * **node** (:code:`Node`) - the descendant node
            * **i** (:code:`int`) - the index of the descendant node
            * **data** (:code:`list[dict[str, Any]]`) - Data

            It should return an parent ID for the node's relationships in the
            conjuction with the ID.

        Returns
        -------
        Stratify
            Itself
        """
        self._parent_id = argpass(optional(parent_id))
        return self

    def set_path(
        self, path: Callable[[Node, int, list[dict[str, Any]]], str]
    ) -> TStratify:
        """
        Sets the :code:`path` accessor to the given function and returns this
        stratify operator.

        If a :code:`path` accessor is set, the :code:`id` and :code:`parent_id`
        accessors are ignored, and a unix-like hierarchy is computed on the
        slash-delimited strings returned by the path accessor, imputing parent
        nodes and ids as necessary.

        Parameters
        ----------
        path : Callable[[Node, int, list[dict[str, Any]]], str]
            Function to call which takes as argument:

            * **node** (:code:`Node`) - the descendant node
            * **i** (:code:`int`) - the index of the descendant node
            * **data** (:code:`list[dict[str, Any]]`) - Data

            It should return the path.

        Returns
        -------
        Stratify
            Itself
        """
        self._path = argpass(optional(path))
        return self

    def get_id(self) -> Callable[[Node, int, list[dict[str, Any]]], str]:
        return self._id

    def get_parent_id(self) -> Callable[[Node, int, list[dict[str, Any]]], str]:
        return self._parent_id

    def get_path(self) -> Callable[[Node, int, list[dict[str, Any]]], str]:
        return self._path


def normalize(path: str) -> str:
    path = str(path)
    i = len(path)
    if path == "":
        return "/"
    if slash(path, i - 1) and not slash(path, i - 2):
        path = path[:-1]
    return path if path[0] == "/" else f"/{path}"


def slash(path: str, i: int) -> str:
    if path[i] == "/":
        k = 0
        i -= 1
        while i > 0 and path[i] == "\\":
            k += 1
            i -= 1
        if (k & 1) == 0:
            return True
    return False


def parent_of(path: str) -> str:
    i = len(path)
    if i < 2:
        return ""
    i -= 1
    while i > 1:
        if slash(path, i):
            break
        i -= 1
    return path[:i]


def stratify() -> Stratify:
    """
    Builds a new stratify operator with the default settings.

    Returns
    -------
    Stratify
        Stratify object
    """
    return Stratify()
