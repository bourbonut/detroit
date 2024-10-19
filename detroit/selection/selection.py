# src/local.py
next_id = 0

class Local:
    def __init__(self):
        global next_id
        next_id += 1
        self._ = "@" + base36(next_id)

    def get(self, node):
        id_ = self._
        while id_ not in node:
            if not (node := node.parentNode):
                return
        return node[id_]

    def set(self, node, value):
        return node[self._] = value

    def remove(self, node):
        if self._ in node:
            del node[self._]

    def __str__(self):
        return self._

def base36(num):
    return base_repr(num, 36)

# ----- 

# src/create.py
from creator import creator
from select import select

def create(name):
    return select(creator(name)(document.documentElement))

# ----- 

# src/pointer.py
from source_event import source_event

def pointer(event, node=None):
    event = source_event(event)
    if node is None:
        node = event.currentTarget
    if node:
        svg = node.ownerSVGElement or node
        if hasattr(svg, 'createSVGPoint'):
            point = svg.createSVGPoint()
            point.x = event.clientX
            point.y = event.clientY
            point = point.matrixTransform(node.getScreenCTM().inverse())
            return [point.x, point.y]
        if hasattr(node, 'getBoundingClientRect'):
            rect = node.getBoundingClientRect()
            return [event.clientX - rect.left - node.clientLeft, event.clientY - rect.top - node.clientTop]
    return [event.pageX, event.pageY]

# ----- 

# src/source_event.py
def source_event(event):
    while (source_event := event.sourceEvent):
        event = source_event
    return event

# ----- 

# src/window.py
def window(node):
    return (node.ownerDocument and node.ownerDocument.defaultView) or (node.document and node) or node.defaultView

# ----- 

# src/select.py
from selection import Selection, root

def select(selector):
    if isinstance(selector, str):
        return Selection([[document.querySelector(selector)]], [document.documentElement])
    return Selection([[selector]], root)

# ----- 

# src/select_all.py
from array import array
from selection import Selection, root

def select_all(selector):
    if isinstance(selector, str):
        return Selection([document.querySelectorAll(selector)], [document.documentElement])
    return Selection([array(selector)], root)

# ----- 

# src/creator.py
from namespace import namespace
from namespaces import xhtml

def creator_inherit(name):
    def create():
        document = self.ownerDocument
        uri = self.namespaceURI
        if uri == xhtml and document.documentElement.namespaceURI == xhtml:
            return document.createElement(name)
        return document.createElementNS(uri, name)
    return create

def creator_fixed(fullname):
    def create():
        return self.ownerDocument.createElementNS(fullname.space, fullname.local)
    return create

def creator(name):
    fullname = namespace(name)
    return creator_fixed(fullname) if fullname.local else creator_inherit(fullname)

# ----- 

# src/namespace.py
from namespaces import namespaces

def namespace(name):
    prefix = name + ""
    i = prefix.find(":")
    if i >= 0 and (prefix := name[:i]) != "xmlns":
        name = name[i + 1:]
    return {'space': namespaces[prefix], 'local': name} if prefix in namespaces else name

# ----- 

# src/pointers.py
from pointer import pointer
from source_event import source_event

def pointers(events, node=None):
    if hasattr(events, 'target'):
        events = source_event(events)
        if node is None:
            node = events.currentTarget
        events = events.touches or [events]
    return [pointer(event, node) for event in events]

# ----- 

# src/namespaces.py
xhtml = "http://www.w3.org/1999/xhtml"

namespaces = {
    'svg': "http://www.w3.org/2000/svg",
    'xhtml': xhtml,
    'xlink': "http://www.w3.org/1999/xlink",
    'xml': "http://www.w3.org/XML/1998/namespace",
    'xmlns': "http://www.w3.org/2000/xmlns/"
}

# ----- 

# src/selector.py
def none():
    return None

def selector(selector):
    return none if selector is None else lambda: self.querySelector(selector)

# ----- 

# src/matcher.py
def matcher(selector):
    return lambda: self.matches(selector)

def child_matcher(selector):
    return lambda node: node.matches(selector)

# ----- 

# src/constant.py
def constant(x):
    return lambda: x

# ----- 

# src/array.py
def array(x):
    return [] if x is None else x if isinstance(x, list) else list(x)

# ----- 

# src/index.py
from create import create
from creator import creator
from local import local
from matcher import matcher
from namespace import namespace
from namespaces import namespaces
from pointer import pointer
from pointers import pointers
from select import select
from select_all import select_all
from selection import selection
from selector import selector
from selector_all import selector_all
from selection.style import style_value as style
from window import window

# ----- 

# src/selector_all.py
def empty():
    return []

def selector_all(selector):
    return empty if selector is None else lambda: self.querySelectorAll(selector)

# ----- 

# src/identity.py
def identity(x):
    return x

# ----- 

# src/selection/node.py
def node():
    for groups in self._groups:
        for group in groups:
            for node in group:
                if node:
                    return node
    return None

# ----- 

# src/selection/insert.py
from creator import creator
from selector import selector

def constant_null():
    return None

def insert(name, before):
    create = name if callable(name) else creator(name)
    select = constant_null if before is None else before if callable(before) else selector(before)
    return self.select(lambda: self.insertBefore(create(*args), select(*args) or None))

# ----- 

# src/selection/append.py
from creator import creator

def append(name):
    create = name if callable(name) else creator(name)
    return self.select(lambda: self.appendChild(create(*args)))

# ----- 

# src/selection/select.py
from selection import Selection
from selector import selector

def select(select):
    if not callable(select):
        select = selector(select)

    for groups in self._groups:
        for group in groups:
            for node in group:
                if node:
                    subnode = select(node, node.__data__, i, group)
                    if "__data__" in node:
                        subnode.__data__ = node.__data__
                    subgroup[i] = subnode

    return Selection(subgroups, self._parents)

# ----- 

# src/selection/enter.py
from sparse import sparse
from selection import Selection

def enter():
    return Selection(self._enter or [sparse(group) for group in self._groups], self._parents)

class EnterNode:
    def __init__(self, parent, datum):
        self.ownerDocument = parent.ownerDocument
        self.namespaceURI = parent.namespaceURI
        self._next = None
        self._parent = parent
        self.__data__ = datum

    def appendChild(self, child):
        return self._parent.insertBefore(child, self._next)

    def insertBefore(self, child, next):
        return self._parent.insertBefore(child, next)

    def querySelector(self, selector):
        return self._parent.querySelector(selector)

    def querySelectorAll(self, selector):
        return self._parent.querySelectorAll(selector)

# ----- 

# src/selection/on.py
def context_listener(listener):
    return lambda event: listener(self, event, self.__data__)

def parse_typenames(typenames):
    return [{'type': t.split('.')[0], 'name': t.split('.')[1] if '.' in t else ''} for t in typenames.strip().split()]

def on_remove(typename):
    return lambda: None  # Implement removal logic

def on_add(typename, value, options):
    return lambda: None  # Implement addition logic

def on(typename, value=None, options=None):
    typenames = parse_typenames(typename + "")
    if value is None:
        on = self.node().__on
        if on:
            for o in on:
                for t in typenames:
                    if t['type'] == o.type and t['name'] == o.name:
                        return o.value
        return

    on = on_add if value else on_remove
    for t in typenames:
        self.each(on(t, value, options))
    return self

# ----- 

# src/selection/exit.py
from sparse import sparse
from selection import Selection

def exit():
    return Selection(self._exit or [sparse(group) for group in self._groups], self._parents)

# ----- 

# src/selection/select_child.py
from matcher import child_matcher

def child_find(match):
    return lambda: next(filter(match, self.children))

def child_first():
    return self.firstElementChild

def select_child(match):
    return self.select(child_first if match is None else child_find(match if callable(match) else child_matcher(match)))

# ----- 

# src/selection/join.py
def join(onenter, onupdate, onexit):
    enter = self.enter()
    update = self
    exit = self.exit()
    if callable(onenter):
        enter = onenter(enter)
        if enter:
            enter = enter.selection()
    else:
        enter = enter.append(onenter + "")
    if onupdate is not None:
        update = onupdate(update)
        if update:
            update = update.selection()
    if onexit is None:
        exit.remove()
    else:
        onexit(exit)
    return enter and update and enter.merge(update).order() or update

# ----- 

# src/selection/empty.py
def empty():
    return not self.node()

# ----- 

# src/selection/select_all.py
from selection import Selection
from array import array
from selector_all import selector_all

def array_all(select):
    return lambda: array(select(*args))

def select_all(select):
    if callable(select):
        select = array_all(select)
    else:
        select = selector_all(select)

    subgroups = []
    parents = []
    for groups in self._groups:
        for group in groups:
            for node in group:
                if node:
                    subgroups.append(select(node, node.__data__, i, group))
                    parents.append(node)

    return Selection(subgroups, parents)

# ----- 

# src/selection/size.py
def size():
    return sum(1 for _ in self)

# ----- 

# src/selection/attr.py
from namespace import namespace

def attr_remove(name):
    return lambda: self.removeAttribute(name)

def attr_remove_ns(fullname):
    return lambda: self.removeAttributeNS(fullname.space, fullname.local)

def attr_constant(name, value):
    return lambda: self.setAttribute(name, value)

def attr_constant_ns(fullname, value):
    return lambda: self.setAttributeNS(fullname.space, fullname.local, value)

def attr_function(name, value):
    return lambda: self.setAttribute(name, value(self))

def attr_function_ns(fullname, value):
    return lambda: self.setAttributeNS(fullname.space, fullname.local, value(self))

def attr(name, value=None):
    fullname = namespace(name)

    if value is None:
        node = self.node()
        return node.getAttributeNS(fullname.space, fullname.local) if fullname.local else node.getAttribute(fullname)

    return self.each(attr_remove_ns(fullname) if value is None else (attr_function_ns(fullname, value) if callable(value) else attr_constant_ns(fullname, value)))

# ----- 

# src/selection/select_children.py
from matcher import child_matcher

def children():
    return list(self.children)

def children_filter(match):
    return lambda: filter(match, self.children)

def select_children(match):
    return self.select_all(children if match is None else children_filter(match if callable(match) else child_matcher(match)))

# ----- 

# src/selection/sparse.py
def sparse(update):
    return [None] * len(update)

# ----- 

# src/selection/each.py
def each(callback):
    for groups in self._groups:
        for group in groups:
            for node in group:
                if node:
                    callback(node, node.__data__, i, group)
    return self

# ----- 

# src/selection/clone.py
def selection_clone_shallow():
    clone = self.cloneNode(False)
    parent = self.parentNode
    return parent.insertBefore(clone, self.nextSibling) if parent else clone

def selection_clone_deep():
    clone = self.cloneNode(True)
    parent = self.parentNode
    return parent.insertBefore(clone, self.nextSibling) if parent else clone

def clone(deep):
    return self.select(selection_clone_deep if deep else selection_clone_shallow)

# ----- 

# src/selection/text.py
def text_remove():
    self.textContent = ""

def text_constant(value):
    return lambda: self.textContent = value

def text_function(value):
    return lambda: self.textContent = value(self) if value(self) is not None else ""

def text(value=None):
    return self.each(text_remove if value is None else (text_function(value) if callable(value) else text_constant(value)))

# ----- 

# src/selection/dispatch.py
from window import default_view

def dispatch_event(node, type_, params):
    window = default_view(node)
    event = window.CustomEvent

    if callable(event):
        event = event(type_, params)
    else:
        event = window.document.createEvent("Event")
        if params:
            event.initEvent(type_, params.bubbles, params.cancelable)
            event.detail = params.detail
        else:
            event.initEvent(type_, False, False)

    node.dispatchEvent(event)

def dispatch_constant(type_, params):
    return lambda: dispatch_event(self, type_, params)

def dispatch_function(type_, params):
    return lambda: dispatch_event(self, type_, params(self))

def dispatch(type_, params):
    return self.each(dispatch_function(type_, params) if callable(params) else dispatch_constant(type_, params))

# ----- 

# src/selection/property.py
def property_remove(name):
    return lambda: del self[name]

def property_constant(name, value):
    return lambda: self[name] = value

def property_function(name, value):
    return lambda: self[name] = value(self)

def property(name, value=None):
    return self.each(property_remove(name) if value is None else (property_function(name, value) if callable(value) else property_constant(name, value)))

# ----- 

# src/selection/datum.py
def datum(value=None):
    return self.property("__data__", value) if value is not None else self.node().__data__

# ----- 

# src/selection/index.py
from select import select
from select_all import select_all
from select_child import select_child
from select_children import select_children
from filter import filter
from data import data
from enter import enter
from exit import exit
from join import join
from merge import merge
from order import order
from sort import sort
from call import call
from nodes import nodes
from node import node
from size import size
from empty import empty
from each import each
from attr import attr
from style import style
from property import property
from classed import classed
from text import text
from html import html
from raise_ import raise_
from lower import lower
from append import append
from insert import insert
from remove import remove
from clone import clone
from datum import datum
from on import on
from dispatch import dispatch
from iterator import iterator

class Selection:
    def __init__(self, groups, parents):
        self._groups = groups
        self._parents = parents

    def select(self, select):
        return select(self)

    def select_all(self, select):
        return select(self)

    def select_child(self, select):
        return select(self)

    def select_children(self, select):
        return select(self)

    def filter(self, match):
        return filter(self)

    def data(self, data):
        return data(self)

    def enter(self):
        return enter(self)

    def exit(self):
        return exit(self)

    def join(self, onenter, onupdate, onexit):
        return join(self, onenter, onupdate, onexit)

    def merge(self, context):
        return merge(self, context)

    def selection(self):
        return self

    def order(self):
        return order(self)

    def sort(self):
        return sort(self)

    def call(self):
        return call(self)

    def nodes(self):
        return nodes(self)

    def node(self):
        return node(self)

    def size(self):
        return size(self)

    def empty(self):
        return empty(self)

    def each(self):
        return each(self)

    def attr(self):
        return attr(self)

    def style(self):
        return style(self)

    def property(self):
        return property(self)

    def classed(self):
        return classed(self)

    def text(self):
        return text(self)

    def html(self):
        return html(self)

    def raise_(self):
        return raise_(self)

    def lower(self):
        return lower(self)

    def append(self):
        return append(self)

    def insert(self):
        return insert(self)

    def remove(self):
        return remove(self)

    def clone(self):
        return clone(self)

    def datum(self):
        return datum(self)

    def on(self):
        return on(self)

    def dispatch(self):
        return dispatch(self)

    def __iter__(self):
        return iterator(self)

# ----- 

# src/selection/lower.py
def lower():
    if self.previousSibling:
        self.parentNode.insertBefore(self, self.parentNode.firstChild)

def lower():
    return self.each(lower)

# ----- 

# src/selection/classed.py
def class_array(string):
    return string.strip().split()

def class_list(node):
    return node.classList if hasattr(node, 'classList') else ClassList(node)

class ClassList:
    def __init__(self, node):
        self._node = node
        self._names = class_array(node.getAttribute("class") or "")

    def add(self, name):
        if name not in self._names:
            self._names.append(name)
            self._node.setAttribute("class", " ".join(self._names))

    def remove(self, name):
        if name in self._names:
            self._names.remove(name)
            self._node.setAttribute("class", " ".join(self._names))

    def contains(self, name):
        return name in self._names

def classed_add(node, names):
    list_ = class_list(node)
    for name in names:
        list_.add(name)

def classed_remove(node, names):
    list_ = class_list(node)
    for name in names:
        list_.remove(name)

def classed_true(names):
    return lambda: classed_add(self, names)

def classed_false(names):
    return lambda: classed_remove(self, names)

def classed_function(names, value):
    return lambda: (classed_add(self, names) if value(self) else classed_remove(self, names))

def classed(name, value=None):
    names = class_array(name)

    if value is None:
        list_ = class_list(self.node())
        return all(list_.contains(name) for name in names)

    return self.each(classed_function(names, value) if callable(value) else (classed_true(names) if value else classed_false(names)))

# ----- 

# src/selection/iterator.py
def iterator():
    for groups in self._groups:
        for group in groups:
            for node in group:
                if node:
                    yield node

# ----- 

# src/selection/data.py
from selection import Selection
from enter import EnterNode
from constant import constant

def bind_index(parent, group, enter, update, exit, data):
    for i in range(len(data)):
        node = group[i]
        if node:
            node.__data__ = data[i]
            update[i] = node
        else:
            enter[i] = EnterNode(parent, data[i])

    for i in range(len(group)):
        node = group[i]
        if node:
            exit[i] = node

def bind_key(parent, group, enter, update, exit, data, key):
    node_by_key_value = {}
    key_values = [None] * len(group)

    for i in range(len(group)):
        node = group[i]
        if node:
            key_value = key(node.__data__, i, group)
            if key_value in node_by_key_value:
                exit[i] = node
            else:
                node_by_key_value[key_value] = node

    for i in range(len(data)):
        key_value = key(data[i], i, data)
        node = node_by_key_value.get(key_value)
        if node:
            update[i] = node
            node.__data__ = data[i]
            del node_by_key_value[key_value]
        else:
            enter[i] = EnterNode(parent, data[i])

    for i in range(len(group)):
        node = group[i]
        if node and node_by_key_value.get(key_values[i]) == node:
            exit[i] = node

def datum(node):
    return node.__data__

def data(value=None, key=None):
    if value is None:
        return [datum(node) for node in self]

    bind = bind_key if key else bind_index
    parents = self._parents
    groups = self._groups

    if not callable(value):
        value = constant(value)

    for j in range(len(groups)):
        parent = parents[j]
        group = groups[j]
        data = arraylike(value(parent, parent.__data__, j, parents))
        enter_group = [None] * len(data)
        update_group = [None] * len(data)
        exit_group = [None] * len(group)

        bind(parent, group, enter_group, update_group, exit_group, data, key)

        for i0 in range(len(data)):
            previous = enter_group[i0]
            if previous:
                i1 = i0 + 1
                while not update_group[i1] and i1 < len(data):
                    i1 += 1
                previous._next = update_group[i1] if i1 < len(data) else None

    update = Selection(update, parents)
    update._enter = enter
    update._exit = exit
    return update

def arraylike(data):
    return data if hasattr(data, 'length') else list(data)

# ----- 

# src/selection/html.py
def html_remove():
    self.innerHTML = ""

def html_constant(value):
    return lambda: self.innerHTML = value

def html_function(value):
    return lambda: self.innerHTML = value(self) if value(self) is not None else ""

def html(value=None):
    return self.each(html_remove if value is None else (html_function(value) if callable(value) else html_constant(value)))

# ----- 

# src/selection/sort.py
from selection import Selection

def sort(compare=None):
    if compare is None:
        compare = ascending

    def compare_node(a, b):
        return (a and b and compare(a.__data__, b.__data__)) or (not a - not b)

    sortgroups = []
    for groups in self._groups:
        sortgroup = []
        for group in groups:
            for node in group:
                if node:
                    sortgroup.append(node)
        sortgroup.sort(compare_node)
        sortgroups.append(sortgroup)

    return Selection(sortgroups, self._parents).order()

def ascending(a, b):
    return (a < b) - (a > b)

# ----- 

# src/selection/filter.py
from selection import Selection
from matcher import matcher

def filter(match):
    if not callable(match):
        match = matcher(match)

    subgroups = []
    for groups in self._groups:
        subgroup = []
        for group in groups:
            for node in group:
                if node and match(node.__data__, i, group):
                    subgroup.append(node)
        subgroups.append(subgroup)

    return Selection(subgroups, self._parents)

# ----- 

# src/selection/order.py
def order():
    for groups in self._groups:
        for group in groups:
            next_node = None
            for node in reversed(group):
                if node:
                    if next_node and (node.compareDocumentPosition(next_node) ^ 4):
                        next_node.parentNode.insertBefore(node, next_node)
                    next_node = node
    return self

# ----- 

# src/selection/nodes.py
def nodes():
    return list(self)

# ----- 

# src/selection/style.py
from window import default_view

def style_remove(name):
    return lambda: self.style.removeProperty(name)

def style_constant(name, value, priority=None):
    return lambda: self.style.setProperty(name, value, priority)

def style_function(name, value, priority=None):
    return lambda: self.style.setProperty(name, value(self), priority) if value(self) is not None else self.style.removeProperty(name)

def style(name, value=None, priority=None):
    if value is not None:
        return self.each(style_remove(name) if value is None else (style_function(name, value, priority) if callable(value) else style_constant(name, value, priority)))
    return style_value(self.node(), name)

def style_value(node, name):
    return node.style.getPropertyValue(name) or default_view(node).getComputedStyle(node, None).getPropertyValue(name)

# ----- 

# src/selection/remove.py
def remove():
    parent = self.parentNode
    if parent:
        parent.removeChild(self)

def remove():
    return self.each(remove)

# ----- 

# src/selection/raise.py
def raise_():
    if self.nextSibling:
        self.parentNode.appendChild(self)

def raise_():
    return self.each(raise_)

# ----- 

# src/selection/merge.py
from selection import Selection

def merge(context):
    selection = context.selection() if hasattr(context, 'selection') else context

    merges = []
    for groups0, groups1 in zip(self._groups, selection._groups):
        merge = []
        for group0, group1 in zip(groups0, groups1):
            node = group0 or group1
            merge.append(node)
        merges.append(merge)

    for j in range(len(merges), len(self._groups)):
        merges.append(self._groups[j])

    return Selection(merges, self._parents)

# ----- 

# src/selection/call.py
def call():
    callback = arguments[0]
    arguments[0] = self
    callback(*arguments)
    return self

# -----
