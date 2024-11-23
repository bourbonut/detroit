from .init import init_range

class ScaleOrdinal:
    def __init__(self):
        self._index = {}
        self._domain = []
        self._range_vals = []
        self._unknown = None

    def __call__(self, d):
        i = self._index.get(d)
        if i is None:
            if self._unknown is not None:
                return self._unknown
            self._domain.append(d)
            i = len(self._domain) - 1
            self._index[d] = i
        length = len(self._range_vals)
        if not length:
            return None
        index = i % length
        if index >= length or index < 0:
            return None
        return self._range_vals[index]

    def domain(self, *args):
        if args:
            self._domain.clear()
            self._index.clear()
            for value in args[0]:
                if value in self._index:
                    continue
                self._domain.append(value)
                self._index[value] = len(self._domain) - 1
            return self
        return self._domain.copy()

    def range(self, *args):
        if args:
            self._range_vals = list(args[0])
            return self
        return self._range_vals.copy()

    def unknown(self, *args):
        if args:
            self._unknown = args[0]
            return self
        return self._unknown

    def copy(self):
        return ScaleOrdinal().domain(self._domain).range(self._range_vals).unknown(self._unknown)

def scale_ordinal(*args):
    return init_range(ScaleOrdinal(), *args)
