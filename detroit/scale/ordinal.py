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

    def set_domain(self, domain):
        self._domain.clear()
        self._index.clear()
        for value in domain:
            if value in self._index:
                continue
            self._domain.append(value)
            self._index[value] = len(self._domain) - 1
        return self

    @property
    def domain(self):
        return self._domain.copy()

    def set_range(self, range_vals):
        self._range_vals = list(range_vals)
        return self

    @property
    def range(self):
        return self._range_vals.copy()

    def set_unknown(self, unknown):
        self._unknown = unknown
        return self

    @property
    def unknown(self):
        return self._unknown

    def copy(self):
        return (
            ScaleOrdinal()
            .set_domain(self.domain)
            .set_range(self.range)
            .set_unknown(self.unknown)
        )


def scale_ordinal(*args):
    return init_range(ScaleOrdinal(), *args)
