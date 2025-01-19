from __future__ import annotations

from collections.abc import Callable, Iterator
from itertools import zip_longest
from typing import Any, Protocol, TypeAlias, overload

from lxml import etree

from .attr import attr_constant, attr_function
from .bind import bind_index, bind_key
from .clone import clone
from .constant import constant
from .enter import EnterNode
from .namespace import namespace
from .matcher import matcher
from .style import style_constant, style_function, style_value
from .text import text_constant, text_function

Data: TypeAlias = Any
Value: TypeAlias = Any


class Accessor(Protocol):
    @overload
    def __call__(self, d: Data) -> Value: ...

    @overload
    def __call__(self, d: Data, i: int) -> Value: ...

    @overload
    def __call__(self, d: Data, i: int, group: list[etree.Element]) -> Value: ...

    def __call__(self, *args) -> Value: ...


def selector(element: etree.Element, selection: str | None = None):
    if selection is None:
        return element
    order = ""
    if ":" in selection:
        selection, order = selection.split(":")
        if order != "last-of-type":
            raise ValueError("Only 'last-of-type' is implemented currently.")
        order = "[last()]"
    if "." in selection:
        tag, class_name = selection.split(".")
        tag = tag or "*"
        class_name = f"[@class='{class_name}']" if class_name else ""
        return element.xpath(f"./*/{tag}{order}{class_name}") + element.xpath(
            f"./{tag}{order}{class_name}"
        )
    return element.xpath(f"./*/{selection}{order}") + element.xpath(
        f"./{selection}{order}"
    )


def creator(node: etree.Element, fullname: dict | None = None):
    return (
        etree.SubElement(node, fullname["local"], attrs=fullname["space"])
        if isinstance(fullname, dict)
        else etree.SubElement(node, fullname)
    )


class Selection:
    """
    A selection is a set of elements from the DOM.
    Typically these elements are identified by selectors such
    as .fancy for elements with the class fancy, or div to
    select DIV elements.

    Selection methods come in two forms, :code:`select` and :code:`select_all`:
    the former selects only the first matching element, while the latter selects
    all matching elements in document order. The top-level selection methods,
    d3.select and d3.select_all, query the entire document; the subselection
    methods, selection.select and selection.select_all, restrict selection to
    descendants of the selected elements.

    By convention, selection methods that return the current selection such
    as selection.attr use four spaces of indent, while methods that return
    a new selection use only two. This helps reveal changes of context by
    making them stick out of the chain:

    Parameters
    ----------
    groups : list[list[etree.Element]]
        List of groups of selected nodes given its parent.
    parents : list[etree.Element]
        List of parents related to groups.
    enter : list[EnterNode] | None = None
        List of placeholder nodes for each datum that had no corresponding
        DOM element in the selection.
    exit : list[etree.Element] = None
        List of existing DOM elements in the selection for which no new datum was found.
    data : dict[etree.Element, Data] | None = None
        Association between nodes and its data

    Examples
    --------

    >>> (
    ...     d3.create("body")
    ...     .append("svg")
    ...     .attr("width", 960)
    ...     .attr("height", 500)
    ...     .append("g")
    ...     .attr("transform", "translate(20, 20)")
    ...     .append("rect")
    ...     .attr("width", 920)
    ...     .attr("height", 460)
    ... )
    """

    def __init__(
        self,
        groups: list[list[etree.Element]],
        parents: list[etree.Element],
        enter: list[EnterNode] | None = None,
        exit: list[etree.Element] = None,
        data: dict[etree.Element, Data] | None = None,
    ):
        self._groups = groups
        self._parents = parents
        self._enter = enter
        self._exit = exit
        self._data = data or {}

    def select(self, selection: str | None = None) -> Selection:
        """
        Selects the first element that matches the specified :code:`selection` string

        Parameters
        ----------
        selection : str | None
            Selection string

        Returns
        -------
        Selection
            Selection of first element

        Examples
        --------

        >>> d3.select("g.ticks")

        Notes
        -----

        Supported strings are :code:`<tag_name>.<class_name>` or `.<class_name>` or `<tag_name>`.
        To get element in reverse order, you can use `<tag_name>:last-of-type`.
        """
        subgroups = [
            selector(node, selection)[:1]
            for group in self._groups
            for node in group
            if node is not None
        ]
        parents = [
            (group[0]._parent if isinstance(group[0], EnterNode) else group[0])
            for group in self._groups
            if group[0] is not None
        ]
        return Selection(subgroups, parents or self._parents, data=self._data)

    def select_all(self, selection: str | None = None) -> Selection:
        """
        Selects all elements that match the specified :code:`selection` string

        Parameters
        ----------
        selection : str | None
            Selection string

        Returns
        -------
        Selection
            Selection of all matched elements

        Examples
        --------

        >>> d3.select_all("g.ticks")

        Notes
        -----

        Supported strings are :code:`<tag_name>.<class_name>` or `.<class_name>` or `<tag_name>`.
        To get element in reverse order, you can use `<tag_name>:last-of-type`.
        """
        subgroups = [
            selector(node, selection)
            for group in self._groups
            for node in group
            if node is not None
        ]
        parents = [
            (group[0]._parent if isinstance(group[0], EnterNode) else group[0])
            for group in self._groups
            if group[0] is not None
        ]
        return Selection(subgroups, parents or self._parents, data=self._data)

    def enter(self) -> Selection:
        """
        Returns the enter selection: placeholder nodes for each datum
        that had no corresponding DOM element in the selection.

        Returns
        -------
        Selection
            Enter selection
        """
        return Selection(
            self._enter or [[None] * len(group) for group in self._groups],
            self._parents,
            data=self._data,
        )

    def exit(self) -> Selection:
        """
        Returns the exit selection: existing DOM elements in the
        selection for which no new datum was found.
        (The exit selection is empty for selections not returned
        by selection.data.)


        Returns
        -------
        Selection
            Exit selection
        """
        return Selection(
            self._exit or [[None] * len(group) for group in self._groups],
            self._parents,
            data=self._data,
        )

    def merge(self, context: Selection) -> Selection:
        """
        Returns a new selection merging this selection with the
        specified other selection or transition. The returned
        selection has the same number of groups and the same parents
        as this selection. Any missing (None) elements in this
        selection are filled with the corresponding element, if
        present (not null), from the specified selection. (If the
        other selection has additional groups or parents, they are
        ignored.)

        Parameters
        ----------
        context : Selection
            Selection

        Returns
        -------
        Selection
            Merged selection
        """
        selection = context.selection() if hasattr(context, "selection") else context

        merges = []
        for groups0, groups1 in zip_longest(
            self._groups, selection._groups, fillvalue=[]
        ):
            merge = []
            for group0, group1 in zip_longest(groups0, groups1, fillvalue=None):
                node = group0 if group0 is not None else group1
                merge.append(node)
            merges.append(merge)

        for j in range(len(merges), len(self._groups)):
            merges.append(self._groups[j])

        return Selection(merges, self._parents, data=self._data | selection._data)

    def filter(self, match: Accessor | int | float | str) -> Selection:
        """
        Filters the selection, returning a new selection that contains
        only the elements for which the specified filter is true.

        Parameters
        ----------
        match : Accessor | int | float | str
            Constant to match or accessor which returns a boolean

        Returns
        -------
        Selection
            Filtered selection

        Examples
        --------
        For example, to filter a selection of table rows to contain only even rows:

        >>> even = d3.select_all("tr").filter(lambda d, i: i % 2 == 0)
        """
        matches, nargs = matcher(match)
        subgroups = []
        for group in self._groups:
            subgroup = []
            for i, node in enumerate(group):
                if node is None:
                    continue
                if isinstance(node, EnterNode):
                    node = node._parent
                args = [self._data.get(node), i, group][:nargs]
                if matches(*args):
                    subgroup.append(node)
            subgroups.append(subgroup)
        return Selection(subgroups, self._parents, data=self._data)


    def append(self, name: str) -> Selection:
        """
        If the specified name is a string, appends a new element
        of this type (tag name) as the last child of each selected
        element, or before the next following sibling in the update
        selection if this is an enter selection. The latter behavior
        for enter selections allows you to insert elements into the
        DOM in an order consistent with the new bound data; however,
        note that selection.order may still be required if updating
        elements change order (i.e., if the order of new data is
        inconsistent with old data).

        Parameters
        ----------
        name : str
            Tag name

        Returns
        -------
        Selection
            Selection

        Examples
        --------

        >>> svg.select_all("g").append("path")
        """
        fullname = namespace(name)
        subgroups = []
        for group in self._groups:
            subgroup = []
            for node in group:
                if node is None:
                    continue
                if isinstance(node, EnterNode):
                    enter_node = node
                    node = enter_node._parent
                    subnode = creator(node, fullname)
                    node.append(subnode)
                    subgroup.append(subnode)
                    self._data[subnode] = enter_node.__data__
                else:
                    subnode = creator(node, fullname)
                    node.append(subnode)
                    subgroup.append(subnode)
                    self._data[subnode] = self._data.get(node)
            subgroups.append(subgroup)
        parents = [
            (group[0]._parent if isinstance(group[0], EnterNode) else group[0])
            for group in self._groups
            if group[0] is not None
        ]
        return Selection(subgroups, parents or self._parents, data=self._data)

    def each(
        self, callback: Callable[[etree.Element, Data, int, list[etree.Element]], None]
    ):
        """
        Invokes the specified function for each selected element,
        in order, being passed the current DOM element (nodes[i]),
        the current datum (d), the current index (i), and the
        current group (nodes).

        Parameters
        ----------
        callback : Callable[[etree.Element, Data, int, list[etree.Element]], None]
            Function to call which takes as argument: node, data, index and group
        """
        for group in self._groups:
            for i, node in enumerate(group):
                if node is not None:
                    if isinstance(node, EnterNode):
                        node = node._parent
                    callback(node, self._data.get(node), i, group)

    def attr(self, name: str, value: Accessor | str | None = None) -> Selection:
        """
        If a value is specified, sets the attribute with the specified name
        to the specified value on the selected elements and returns this selection.

        If the value is a function, it is evaluated for each selected element,
        in order, being passed the current datum (d), the current index (i),
        and the current group (nodes).

        Parameters
        ----------
        name : str
            Name of the attribute
        value : Accessor | str | None
            Value

        Returns
        -------
        Selection
            Itself

        Examples
        --------

        >>> selection.attr("color", "red")
        """
        if value is None:
            return self.node().get(name)
        elif callable(value):
            self.each(attr_function(name, value))
        else:
            self.each(attr_constant(name, value))
        return self

    def style(self, name: str, value: Accessor | str | None = None) -> Selection:
        """
        If a value is specified, sets the style with the specified name
        to the specified value on the selected elements and returns this selection.

        If the value is a function, it is evaluated for each selected element,
        in order, being passed the current datum (d), the current index (i),
        and the current group (nodes).

        Parameters
        ----------
        name : str
            Name of the style
        value : Accessor | str | None
            Value constant or function

        Returns
        -------
        Selection
            Itself

        Examples
        --------

        >>> selection.style("color", "red")
        """
        if value is None:
            return style_value(self.nodes.get(name).get("style"), name)
        elif callable(value):
            self.each(style_function(name, value))
        else:
            self.each(style_constant(name, value))
        return self

    def text(self, value: Accessor | str | None = None) -> Selection:
        """
        If the value is a constant, then all elements are given the same
        text content; otherwise, if the value is a function, it is evaluated
        for each selected element, in order, being passed the current
        datum (d), the current index (i), and the current group (nodes).

        Parameters
        ----------
        value : Accessor | str | None
            Value constant or function

        Returns
        -------
        Selection
            Itself

        Examples
        --------

        >>> selection.text("Hello, world!")
        """
        if value is None:
            return self.node().get("text")
        elif callable(value):
            self.each(text_function(value))
        else:
            self.each(text_constant(value))
        return self

    def datum(self, value: Data) -> Selection:
        """
        Sets the bound data for the first selected node.

        Parameters
        ----------
        value : Data
            Value

        Returns
        -------
        Selection
            Itself
        """
        self._data[self.node()] = value
        return self

    def data(self, values: list[Data], key: Accessor | None = None) -> Selection:
        """
        Binds the specified list of data with the selected elements,
        returning a new selection that represents the update selection:
        the elements successfully bound to data. Also defines the enter
        and exit selections on the returned selection, which can be used
        to add or remove elements to correspond to the new data. The
        specified data is an array of arbitrary values (e.g., numbers or
        objects), or a function that returns an array of values for each
        group.

        Parameters
        ----------
        values : list[Data]
            List of data to bind
        key : Accessor | None
            Optional accessor which returns a key value

        Returns
        -------
        Selection
            Itself
        """
        bind = bind_key if key else bind_index
        parents = self._parents
        groups = self._groups

        if not callable(values):
            values = constant(values)

        update = [None] * len(groups)
        enter = [None] * len(groups)
        exit = [None] * len(groups)
        for j in range(len(groups)):
            parent = parents[j]
            group = groups[j]
            data = list(values(parent, self._data.get(parent), j, parents))
            enter[j] = enter_group = [None] * len(data)
            update[j] = update_group = [None] * len(data)
            exit[j] = exit_group = [None] * len(group)

            bind(
                self._data,
                parent,
                group,
                enter_group,
                update_group,
                exit_group,
                data,
                key,
            )

            i1 = 0
            for i0 in range(len(data)):
                if previous := enter_group[i0]:
                    if i0 >= i1:
                        i1 = i0 + 1
                    while not (
                        i1 < len(update_group) and update_group[i1] is not None
                    ) and i1 < len(data):
                        i1 += 1
                    previous._next = update_group[i1] if i1 < len(data) else None

        return Selection(update, parents, enter, exit, self._data)

    def order(self) -> Selection:
        """
        Re-inserts elements into the document such that the document order
        of each group matches the selection order.

        Returns
        -------
        Selection
            Itself
        """
        for group in self._groups:
            next_node = None
            for node in reversed(group):
                if node is not None:
                    if next_node is not None and (node.getprevious() == next_node):
                        parent = next_node.getparent()
                        index = parent.index(next_node)
                        parent.pop(index)
                        parent.insert(index, node)
                    next_node = node
        return self

    def join(
        self,
        onenter: Callable | Selection,
        onupdate: Callable | None = None,
        onexit: Callable | None = None,
    ):
        """
        Appends, removes and reorders elements as necessary to match
        the data that was previously bound by selection.data, returning
        the merged enter and update selection. This method is a convenient
        alternative to the explicit general update pattern, replacing
        selection.enter, selection.exit, selection.append, selection.remove, and selection.order.

        Parameters
        ----------
        onenter : Callable | Selection
            Enter selection or function
        onupdate : Callable | None
            Function
        onexit : Callable | None
            Function

        Returns
        -------
            Selection with joined elements
        """
        enter = self.enter()
        update = self
        exit = self.exit()

        # Enter
        if callable(onenter):
            enter = onenter(enter)
            if enter:
                enter = enter.selection()
        else:
            enter = enter.append(onenter)

        # Update
        if onupdate is not None:
            update = onupdate(update)
            if update:
                update = update.selection()

        # Exit
        if onexit is None:
            exit.remove()
        else:
            onexit(exit)

        if enter and update:
            return enter.merge(update).order()
        else:
            return update

    def insert(self, name: str, before: etree.Element) -> Selection:
        """
        If the specified name is a string, inserts a new element
        of this type (tag name) before the first element matching
        the specified before selector for each selected element.

        Parameters
        ----------
        name : str
            Tag name
        before : etree.Element
            Node element

        Returns
        -------
        Selection
            Itself with inserted element
        """
        fullname = namespace(name)
        for group in self._groups:
            for i, node in enumerate(group):
                if node is not None:
                    if isinstance(node, EnterNode):
                        node = node._parent
                    selection = selector(node, before)
                    if selection := [
                        found for found in selection if found.getparent() == node
                    ]:
                        index = node.index(selection[0])
                        created = creator(node, fullname)
                        node.insert(index, created)
                        group[i] = created
        return self

    def remove(self) -> Selection:
        """
        Removes the selected elements from the document. Returns this
        selection (the removed elements) which are now detached from
        the DOM.

        Returns
        -------
        Selection
            Itself with removed elements
        """

        def remove(node, data, i, group):
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)

        self.each(remove)
        return self

    def call(self, func: Callable[[Selection, ...], Any], *args: Data) -> Selection:
        """
        Invokes the specified function exactly once, passing in
        this selection along with any optional arguments. Returns
        this selection.

        Parameters
        ----------
        func : Callable[[Selection, ...], Any]
            Function to call
        args : Data
            Arguments for the function to call

        Returns
        -------
        Selection
            Itself

        Examples
        --------

        This is equivalent to invoking the function
        by hand but facilitates method chaining. For example, to set
        several styles in a reusable function:

        >>> def name(selection, first, last):
        ...     selection.attr("first-name", first).attr("last-name", last)

        Now say:
        >>> d3.select_all("div").call(name, "John", "Snow")

        This is roughly equivalent to:

        >>> name(d3.select_all("div"), "John", "Snow")
        """
        func(self, *args)
        return self

    def clone(self) -> Selection:
        """
        Inserts clones of the selected elements immediately following
        the selected elements and returns a selection of the newly
        added clones.

        Returns
        -------
        Selection
            Clone of itself
        """
        subgroups = [
            clone(node) for group in self._groups for node in group if node is not None
        ]
        return Selection(subgroups, self._parents, data=self._data)

    def node(self) -> etree.Element:
        """
        Returns the first (non-None) element in this selection.

        Returns
        -------
        etree.Element
            Node
        """
        return next(iter(self))

    def nodes(self) -> list[etree.Element]:
        """
        Returns a list of all (non-None) elements in this selection.

        Returns
        -------
        list[etree.Element]
            List of nodes
        """
        return list(self)

    def __iter__(self) -> Iterator[etree.Element]:
        """
        Make the selection as an iterator

        Returns
        -------
        Iterator[etree.Element]
            Iterator of non-None nodes
        """
        for group in self._groups:
            for node in group:
                if node is not None:
                    yield node

    def selection(self) -> Selection:
        """
        Returns the selection

        Returns
        -------
        Selection
            Itself
        """
        return self

    def to_string(self, pretty_print: bool = True) -> str:
        """
        Convert selection to string

        Parameters
        ----------
        pretty_print : bool
            :code:`True` to prettify output

        Returns
        -------
        str
            String
        """
        return etree.tostring(self._parents[0], pretty_print=pretty_print).decode(
            "utf-8"
        )

    def __str__(self) -> str:
        """
        Returns the SVG content

        Returns
        -------
        str
            String
        """
        return self.to_string(False)

    def __repr__(self) -> str:
        """
        Represents the selection

        Returns
        -------
        str
            String
        """

        def node_repr(node):
            if node is None:
                return str(node)
            if isinstance(node, EnterNode):
                return str(node)
            tag = node.tag
            class_name = node.attrib.get("class")
            if class_name:
                return f"{tag}.{class_name}"
            return tag

        groups = [
            f"[{', '.join(node_repr(node) for node in group)}]"
            for group in self._groups
        ]
        parents = f"[{', '.join(node_repr(parent) for parent in self._parents)}]"
        return (
            f"Selection(\n    groups=[{', '.join(groups)}],\n    parents={parents},"
            f"\n    enter={self._enter},\n    exit={self._exit},\n    data={self._data},\n)"
        )
