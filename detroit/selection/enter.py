class EnterNode:
    def __init__(self, parent, datum):
        self._next = None
        self._parent = parent
        self.__data__ = datum

    def __str__(self):
        if self._parent is None:
            return f"EnterNode({self._parent}, {self.__data__})"
        tag = self._parent.tag
        class_name = self._parent.attrib.get("class")
        if class_name:
            return f"EnterNode({tag}.{class_name}, {self.__data__})"
        return f"EnterNode({tag}, {self.__data__})"

    def __repr__(self):
        return str(self)

    # def append_child(self, child):
    #     return self._parent.insert_before(child, self._next)
    #
    # def insert_before(self, child, next):
    #     return self._parent.insert_before(child, next)
    #
    # def query_selector(self, selector):
    #     return self._parent.query_selector(selector)
    #
    # def query_selector_all(self, selector):
    #     return self._parent.query_selector_all(selector)
