from time import perf_counter

from collections import defaultdict
from collections.abc import Callable, Iterator
from itertools import zip_longest
from inspect import signature
from typing import Any, Protocol, TypeAlias, TypeVar, overload

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
from ..types import Data, Value, Accessor

TSelection = TypeVar("Selection", bound="Selection")

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
        return element.xpath(f"./*//{tag}{order}{class_name}") + element.xpath(
            f"./{tag}{order}{class_name}"
        )
    return element.xpath(f"./*//{selection}{order}") + element.xpath(
        f"./{selection}{order}"
    )


def creator(node: etree.Element, fullname: dict | None = None):
    return (
        etree.SubElement(node, fullname["local"], nsmap=fullname["space"])
        if isinstance(fullname, dict)
        else etree.SubElement(node, fullname, nsmap={})
    )


class Selection:
    """
    A selection is a set of elements from the DOM. Typically these elements are
    identified by selectors such as .fancy for elements with the class fancy,
    or div to select DIV elements.

    Selection methods come in two forms, :code:`select` and :code:`select_all`:
    the former selects only the first matching element, while the latter
    selects all matching elements in document order. The top-level selection
    methods, d3.select and d3.select_all, query the entire document; the
    subselection methods, selection.select and selection.select_all, restrict
    selection to descendants of the selected elements.

    By convention, selection methods that return the current selection such as
    selection.attr use four spaces of indent, while methods that return a new
    selection use only two. This helps reveal changes of context by making them
    stick out of the chain:

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

    >>> body = d3.create("body")
    >>> (
    ...     body
    ...     .append("svg")
    ...     .attr("width", 960)
    ...     .attr("height", 500)
    ...     .append("g")
    ...     .attr("transform", "translate(20, 20)")
    ...     .append("rect")
    ...     .attr("width", 920)
    ...     .attr("height", 460)
    ... )
    >>> print(body.to_string())
    <body>
      <svg xmlns="http://www.w3.org/2000/svg" weight="960" height="500">
        <g transform="translate(20, 20)">
          <rect width="920" height="460"/>
        </g>
      </svg>
    </body>
    >>> str(body)
    '<body><svg xmlns="http://www.w3.org/2000/svg" weight="960" height="500"><g transform="translate(20, 20)"><rect width="920" height="460"/></g></svg></body>'
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

    def select(self, selection: str | None = None) -> TSelection:
        """
        Selects the first element that matches the specified :code:`selection` string.

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

        >>> svg = d3.create("svg")
        >>> svg.append("g").attr("class", "ticks")
        Selection(
            groups=[[g.ticks]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f2d1504cb80>: None},
        )
        >>> svg.append("g").attr("class", "labels")
        Selection(
            groups=[[g.labels]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f2d1504cb80>: None, <Element g at 0x7f2d15052640>: None},
        )
        >>> svg.select("g.ticks")
        Selection(
            groups=[[g.ticks]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f2d1504cb80>: None, <Element g at 0x7f2d15052640>: None},
        )
        >>> svg.select("g.points")
        Selection(
            groups=[[]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f2d1504cb80>: None, <Element g at 0x7f2d15052640>: None},
        )

        Notes
        -----

        Supported strings are :code:`<tag_name>.<class_name>` or
        :code:`.<class_name>` or :code:`<tag_name>`. To get element in reverse
        order, you can use :code:`<tag_name>:last-of-type`.
        """
        groups = defaultdict(list)
        nodes = (node for group in self._groups for node in group)
        for node in filter(lambda n: n is not None, nodes):
            subgroup = selector(node, selection)[:1]
            if len(subgroup) == 0:
                groups[node]
                continue
            for subnode in subgroup:
                parent = subnode.getparent()
                groups[parent].append(subnode)

        subgroups = list(groups.values())
        parents = list(groups)

        return Selection(subgroups, parents or self._parents, data=self._data)

    def select_all(self, selection: str | None = None) -> TSelection:
        """
        Selects all elements that match the specified :code:`selection` string.

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

        >>> svg = d3.create("svg")
        >>> scale = d3.scale_linear([0, 10], [0, 100])
        >>> print(svg.call(d3.axis_bottom(scale).set_ticks(3)).to_string())
        <svg xmlns:xmlns="http://www.w3.org/2000/svg" fill="none" font-size="10" font-family="sans-serif" text-anchor="middle">
          <path class="domain" stroke="currentColor" d="M0.5,6V0.5H100.5V6"/>
          <g class="tick" opacity="1" transform="translate(0.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0</text>
          </g>
          <g class="tick" opacity="1" transform="translate(50.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">5</text>
          </g>
          <g class="tick" opacity="1" transform="translate(100.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">10</text>
          </g>
        </svg>
        >>> svg.select_all("g").select_all("line")
        Selection(
            groups=[[line], [line], [line]],
            parents=[g.tick, g.tick, g.tick],
            enter=None,
            exit=None,
            data={},
        )
        >>> svg.select_all("line")
        Selection(
            groups=[[line], [line], [line]],
            parents=[g.tick, g.tick, g.tick],
            enter=None,
            exit=None,
            data={},
        )

        Notes
        -----

        Supported strings are :code:`<tag_name>.<class_name>` or
        :code:`.<class_name>` or :code:`<tag_name>`. To get element in reverse
        order, you can use :code:`<tag_name>:last-of-type`.
        """
        groups = defaultdict(list)
        nodes = (node for group in self._groups for node in group)
        for node in filter(lambda n: n is not None, nodes):
            subgroup = selector(node, selection)
            if len(subgroup) == 0:
                groups[node]
                continue
            for subnode in subgroup:
                parent = subnode.getparent()
                groups[parent].append(subnode)

        subgroups = list(groups.values())
        parents = list(groups)
                
        return Selection(subgroups, parents, data=self._data)

    def enter(self) -> TSelection:
        """
        Returns the enter selection: placeholder nodes for each datum that had
        no corresponding DOM element in the selection.

        Returns
        -------
        Selection
            Enter selection

        Examples
        --------

        >>> svg = d3.create("svg")
        >>> text = svg.select_all("text").data(["hello", "world"])
        >>> text_enter = text.enter()
        >>> text_enter
        Selection(
            groups=[[EnterNode(svg, hello), EnterNode(svg, world)]],
            parents=[svg],
            enter=None,
            exit=None,
            data={},
        )
        """
        return Selection(
            self._enter or [[None] * len(group) for group in self._groups],
            self._parents,
            data=self._data,
        )

    def exit(self) -> TSelection:
        """
        Returns the exit selection: existing DOM elements in the selection for
        which no new datum was found. (The exit selection is empty for
        selections not returned by selection.data.)


        Returns
        -------
        Selection
            Exit selection

        Examples
        --------

        >>> svg = d3.create("svg")
        >>> text = svg.select_all("text").data(["hello", "world"])
        >>> text_exit = text.exit()
        >>> text_exit
        Selection(
            groups=[[]],
            parents=[svg],
            enter=None,
            exit=None,
            data={},
        )
        """
        return Selection(
            self._exit or [[None] * len(group) for group in self._groups],
            self._parents,
            data=self._data,
        )

    def merge(self, context: TSelection) -> TSelection:
        """
        Returns a new selection merging this selection with the specified other
        selection or transition. The returned selection has the same number of
        groups and the same parents as this selection. Any missing (None)
        elements in this selection are filled with the corresponding element,
        if present (not null), from the specified selection. (If the other
        selection has additional groups or parents, they are ignored.)

        Parameters
        ----------
        context : Selection
            Selection

        Returns
        -------
        Selection
            Merged selection

        Examples
        --------

        >>> svg = d3.create("svg")
        >>> text = svg.select_all("text").data(["hello", "world"])
        >>> text_enter = text.enter()
        >>> text_enter.append("text").text(lambda text: text)
        Selection(
            groups=[[text, text]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element text at 0x7f2d14b2a580>: 'hello', <Element text at 0x7f2d14457540>: 'world'},
        )
        >>> print(svg.to_string())
        <svg xmlns:xmlns="http://www.w3.org/2000/svg">
          <text>hello</text>
          <text>world</text>
        </svg>
        >>> text
        Selection(
            groups=[[None, None]],
            parents=[svg],
            enter=[[EnterNode(svg, hello), EnterNode(svg, world)]],
            exit=[[]],
            data={},
        )
        >>> text = text.merge(text_enter)
        >>> text
        Selection(
            groups=[[EnterNode(svg, hello), EnterNode(svg, world)]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element text at 0x7f2d14b2a580>: 'hello', <Element text at 0x7f2d14457540>: 'world'},
        )
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

    def filter(self, match: Accessor | int | float | str) -> TSelection:
        """
        Filters the selection, returning a new selection that contains only the
        elements for which the specified filter is true.

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

        >>> svg = d3.create("svg")
        >>> scale = d3.scale_linear([0, 10], [0, 100])
        >>> print(svg.call(d3.axis_bottom(scale).set_ticks(3)).to_string())
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" font-size="10" font-family="sans-serif" text-anchor="middle">
          <path class="domain" stroke="currentColor" d="M0.5,6V0.5H100.5V6"/>
          <g class="tick" opacity="1" transform="translate(0.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0</text>
          </g>
          <g class="tick" opacity="1" transform="translate(50.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">5</text>
          </g>
          <g class="tick" opacity="1" transform="translate(100.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">10</text>
          </g>
        </svg>
        >>> result = svg.select_all("text").filter(lambda d, i: i % 2 != 0)
        >>> result
        Selection(
            groups=[[text]],
            parents=[svg],
            enter=None,
            exit=None,
            data={},
        )
        >>> result.node().text
        '5'
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


    def append(self, name: str) -> TSelection:
        """
        If the specified name is a string, appends a new element of this type
        (tag name) as the last child of each selected element, or before the
        next following sibling in the update selection if this is an enter
        selection. The latter behavior for enter selections allows you to
        insert elements into the DOM in an order consistent with the new bound
        data; however, note that selection.order may still be required if
        updating elements change order (i.e., if the order of new data is
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

        >>> svg = d3.create("svg")
        >>> print(svg.to_string())
        <svg xmlns="http://www.w3.org/2000/svg"/>
        >>> g = svg.append("g").attr("class", "labels")
        >>> print(svg.to_string())
        <svg xmlns="http://www.w3.org/2000/svg">
          <g class="labels"/>
        </svg>
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
        Invokes the specified function for each selected element, in order,
        being passed the current DOM element (nodes[i]), the current datum (d),
        the current index (i), and the current group (nodes).

        Parameters
        ----------
        callback : Callable[[etree.Element, Data, int, list[etree.Element]], None]
            Function to call which takes as argument:

            * **node** (`etree.Element`) - the node element
            * **data** (`Any`) - current data associated to the node
            * **index** (`int`) - the index of the node in its group
            * **group** (`list[etree.Element]`) - the node's group with other nodes.
        """
        for group in self._groups:
            for i, node in enumerate(group):
                if node is not None:
                    if isinstance(node, EnterNode):
                        node = node._parent
                    callback(node, self._data.get(node), i, group)

    def attr(self, name: str, value: Accessor | str | None = None) -> TSelection:
        """
        If a value is specified, sets the attribute with the specified name to
        the specified value on the selected elements and returns this
        selection.

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

        >>> svg = d3.create("svg")
        >>> print(
        ...     svg.append("g")
        ...     .attr("class", "labels")
        ...     .attr("transform", "translate(20, 10)")
        ...     .to_string()
        ... )
        <svg xmlns="http://www.w3.org/2000/svg">
          <g class="labels" transform="translate(20, 10)"/>
        </svg>
        """
        if value is None:
            return self.node().get(name)
        elif callable(value):
            self.each(attr_function(name, value))
        else:
            self.each(attr_constant(name, value))
        return self

    def style(self, name: str, value: Accessor | str | None = None) -> TSelection:
        """
        If a value is specified, sets the style with the specified name to the
        specified value on the selected elements and returns this selection.

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

        >>> svg = d3.create("svg")
        >>> print(
        ...     svg.append("text")
        ...     .style("fill", "black")
        ...     .style("stroke", "none")
        ...     .to_string()
        ... )
        <svg xmlns="http://www.w3.org/2000/svg">
          <text style="fill:black;stroke:none;"/>
        </svg>
        """
        if value is None:
            return style_value(self.nodes.get(name).get("style"), name)
        elif callable(value):
            self.each(style_function(name, value))
        else:
            self.each(style_constant(name, value))
        return self

    def text(self, value: Accessor | str | None = None) -> TSelection:
        """
        If the value is a constant, then all elements are given the same text
        content; otherwise, if the value is a function, it is evaluated for
        each selected element, in order, being passed the current datum (d),
        the current index (i), and the current group (nodes).

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

        Direct assignment:

        >>> svg = d3.create("svg")
        >>> print(svg.append("text").text("Hello, world!").to_string())
        <svg xmlns="http://www.w3.org/2000/svg">
          <text>Hello, world!</text>
        </svg>

        Through data:

        >>> svg = d3.create("svg")
        >>> print(
        ...     svg.select_all("text")
        ...     .data(["Hello", "world"])
        ...     .enter()
        ...     .append("text")
        ...     .text(lambda text, i: f"{text} - index {i}")
        ...     .to_string()
        ... )
        <svg xmlns="http://www.w3.org/2000/svg">
          <text>Hello - index 0</text>
          <text>world - index 1</text>
        </svg>
        
        """
        if value is None:
            return self.node().get("text")
        elif callable(value):
            self.each(text_function(value))
        else:
            self.each(text_constant(value))
        return self

    def datum(self, value: Data) -> TSelection:
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

        Examples
        --------

        >>> svg = d3.create("svg")
        >>> g1 = svg.append("g").attr("class", "g1")
        >>> g2 = svg.append("g").attr("class", "g2")
        >>> g = svg.select_all("g")
        >>> g
        Selection(
            groups=[[g.g1, g.g2]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f3eda0be4c0>: None, <Element g at 0x7f3eda029700>: None},
        )
        >>> g.datum("Hello, world")
        Selection(
            groups=[[g.g1, g.g2]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f3eda0be4c0>: 'Hello, world', <Element g at 0x7f3eda029700>: None},
        )
        >>> g1.node()
        <Element g at 0x7f3eda0be4c0>
        """
        self._data[self.node()] = value
        return self

    def data(self, values: list[Data] | Accessor, key: Accessor | None = None) -> TSelection:
        """
        Binds the specified list of data with the selected elements, returning
        a new selection that represents the update selection: the elements
        successfully bound to data. Also defines the enter and exit selections
        on the returned selection, which can be used to add or remove elements
        to correspond to the new data. The specified data is an array of
        arbitrary values (e.g., numbers or objects), or a function that returns
        an array of values for each group.

        Parameters
        ----------
        values : list[Data] | Accessor
            List of data to bind
        key : Accessor | None
            Optional accessor which returns a key value

        Returns
        -------
        Selection
            Itself

        Examples
        --------

        >>> svg = d3.create("svg")
        >>> svg.append("g")
        Selection(
            groups=[[g]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f3eda09b540>: None},
        )
        >>> svg.append("g")
        Selection(
            groups=[[g]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element g at 0x7f3eda09b540>: None, <Element g at 0x7f3edac50240>: None},
        )
        >>> svg.select_all("text").data(["Hello", "world"])
        Selection(
            groups=[[None, None]],
            parents=[svg],
            enter=[[EnterNode(svg, Hello), EnterNode(svg, world)]],
            exit=[[]],
            data={<Element g at 0x7f3eda09b540>: None, <Element g at 0x7f3edac50240>: None},
        )
        >>> svg.select_all("g").data(["Hello", "world"])
        Selection(
            groups=[[g, g]],
            parents=[svg],
            enter=[[None, None]],
            exit=[[None, None]],
            data={<Element g at 0x7f3eda09b540>: 'Hello', <Element g at 0x7f3edac50240>: 'world'},
        )
        """
        bind = bind_key if key else bind_index
        parents = self._parents
        groups = self._groups

        if not callable(values):
            values = constant(values)
        nargs = len(signature(values).parameters)

        update = [None] * len(groups)
        enter = [None] * len(groups)
        exit = [None] * len(groups)
        for j in range(len(groups)):
            parent = parents[j]
            group = groups[j]
            args = [parent, self._data.get(parent), j, parents][:nargs]
            data = list(values(*args))
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

    def order(self) -> TSelection:
        """
        Re-inserts elements into the document such that the document order of
        each group matches the selection order.

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
        onenter: Callable[[TSelection], TSelection] | str,
        onupdate: Callable[[TSelection], TSelection] | None = None,
        onexit: Callable[[TSelection], None] | None = None,
    ) -> TSelection:
        """
        Appends, removes and reorders elements as necessary to match the data
        that was previously bound by selection.data, returning the merged enter
        and update selection. This method is a convenient alternative to the
        explicit general update pattern, replacing selection.enter,
        selection.exit, selection.append, selection.remove, and
        selection.order.

        Parameters
        ----------
        onenter : Callable[[Selection], Selection] | str
            Enter selection or function
        onupdate : Callable[[Selection], Selection] | None
            Function
        onexit : Callable[[Selection], None] | None
            Function

        Returns
        -------
        Selection
            Selection with joined elements

        Examples
        --------

        >>> data = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        >>> svg = d3.create("svg")
        >>> table = (
        ...     svg.append("table")
        ...     .select_all("tr")
        ...     .data(data)
        ...     .join("tr")
        ...     .select_all("td")
        ...     .data(lambda _, d: d)
        ...     .join("td")
        ...     .text(lambda d: str(d))
        ... )
        >>> print(svg.to_string())
        <svg xmlns="http://www.w3.org/2000/svg">
          <table>
            <tr>
              <td>0</td>
              <td>1</td>
              <td>2</td>
              <td>3</td>
            </tr>
            <tr>
              <td>4</td>
              <td>5</td>
              <td>6</td>
              <td>7</td>
            </tr>
            <tr>
              <td>8</td>
              <td>9</td>
              <td>10</td>
              <td>11</td>
            </tr>
            <tr>
              <td>12</td>
              <td>13</td>
              <td>14</td>
              <td>15</td>
            </tr>
          </table>
        </svg>

        Another usage could be to specify functions :

        >>> svg = d3.create("svg")
        >>> svg.append("circle").attr("fill", "yellow")
        Selection(
            groups=[[circle]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element circle at 0x7f5e219fd300>: None},
        )
        >>> print(svg.to_string())
        <svg xmlns="http://www.w3.org/2000/svg">
          <circle fill="yellow"/>
        </svg>
        >>> (
        ...     svg.select_all("circle")
        ...     .data(data)
        ...     .join(
        ...         onenter=lambda enter: enter.append("circle").attr("fill", "green"),
        ...         onupdate=lambda update: update.attr("fill", "blue")
        ...     )
        ...     .attr("stroke", "black")
        ... )
        Selection(
            groups=[[circle, circle, None]],
            parents=[svg],
            enter=None,
            exit=None,
            data={<Element circle at 0x7f5e219fd300>: 0, <Element circle at 0x7f5e2251f040>: 1, <Element circle at 0x7f5e22517a80>: 2},
        )
        >>> print(svg.to_string())
        <svg xmlns="http://www.w3.org/2000/svg">
          <circle fill="blue"/>
          <circle fill="green" stroke="black"/>
          <circle fill="green" stroke="black"/>
        </svg>

        In this example, the attribute :code:`fill` of the existing circle was
        updated, by :code:`onupdate`, from :code:`yellow` to :code:`blue`. And
        since :code:`data` has 3 elements, :code:`onenter` has generated the
        last circles.
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

    def insert(self, name: str, before: str) -> TSelection:
        """
        If the specified name is a string, inserts a new element of this type
        (tag name) before the first element matching the specified
        :code:`before` selector for each selected element.

        Parameters
        ----------
        name : str
            Tag name
        before : str
            Node element selection

        Returns
        -------
        Selection
            Selection with inserted element(s)
        """
        print(repr(self))
        print(name, before)
        fullname = namespace(name)
        subgroups = []
        for group in self._groups:
            subgroup = []
            for node in group:
                if node is not None:
                    if isinstance(node, EnterNode):
                        node = node._parent
                    selection = selector(node, before)
                    # parents = defaultdict(list)
                    # for found in selection:
                    #     parent = found.getparent()
                    #     parents[parent].append(found)
                    #
                    # for parent, selection in parents.items():
                    if len(selection) > 0:
                        found = selection[0]
                        parent = found.getparent()
                        index = parent.index(found)
                        created = creator(parent, fullname)
                        parent.insert(index, created)
                        self._data[created] = self._data.get(node)
                        subgroup.append(created)
                        # subgroup.append(node)
                    else:
                        subgroup.append(node)
                else:
                    subgroup.append(node)
            subgroups.append(subgroup)

        print(repr(Selection(subgroups, self._parents, data=self._data)))
        print("=" * 142)
        return Selection(subgroups, self._parents, data=self._data)

    def remove(self) -> TSelection:
        """
        Removes the selected elements from the document. Returns this selection
        (the removed elements) which are now detached from the DOM.

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

    def call(self, func: Callable[[TSelection, ...], Any], *args: Data) -> TSelection:
        """
        Invokes the specified function exactly once, passing in this selection
        along with any optional arguments. Returns this selection.

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

    def clone(self) -> TSelection:
        """
        Inserts clones of the selected elements immediately following the
        selected elements and returns a selection of the newly added clones.

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

    def selection(self) -> TSelection:
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
        return (
            etree.tostring(self._parents[0], pretty_print=pretty_print)
            .decode("utf-8")
            .removesuffix("\n")
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
