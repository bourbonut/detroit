class EnterNode:
    def __init__(self, parent, datum):
        self._next = None
        self._parent = parent
        self.__data__ = datum

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
