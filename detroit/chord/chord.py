from functools import cmp_to_key
from collections.abc import Callable, Iterator
from typing import Any, TypeVar
from math import pi

TAU = 2 * pi

TChord = TypeVar("Chord", bound="Chord")


class ChordValue:
    """
    Chord subgroup

    Attributes
    ----------
    index : int
        The node index i
    start_angle : float
        The start angle in radians
    end_angle : float
        The end angle in radians
    value : float
        The flow value matrix[i][j]
    """
    __slots__ = ("index", "start_angle", "end_angle", "value")

    def __init__(self, index: int, start_angle: float, end_angle: float, value: float):
        self.index = index
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.value = value

    def get(self, key: str, default: Any | None = None) -> int | float | None:
        match key:
            case "index":
                return self.index
            case "start_angle":
                return self.start_angle
            case "end_angle":
                return self.end_angle
            case "value":
                return self.value
            case _:
                return default

    def __getitem__(self, key: str) -> int | float:
        value = self.get(key)
        if value is None:
            raise KeyError(f"'ChordValue' object has no attribute {key!r}")
        return value

    def __str__(self) -> str:
        return f"ChordValue({self.index}, {self.start_angle}, {self.end_angle}, {self.value})"

    def __repr__(self) -> str:
        return str(self)

class ChordItem:
    """
    Chord object containing source and target subgroups

    Attributes
    ----------
    source : ChordValue | None
        The source subgroup
    target : ChordValue | None
        The target subgroup
    """
    __slots__ = ("source", "target")

    def __init__(
        self, source: ChordValue | None = None, target: ChordValue | None = None
    ):
        self.source = source
        self.target = target

    def get(self, key: str, default: Any | None = None) -> int | float | None:
        match key:
            case "source":
                return self.source
            case "target":
                return self.target
            case _:
                return default

    def __getitem__(self, key: str) -> int | float:
        value = self.get(key)
        if value is None:
            raise KeyError(f"'ChordItem' object has no attribute {key!r}")
        return value

    def __str__(self) -> str:
        return f"ChordItem({self.source}, {self.target})"

    def __repr__(self) -> str:
        return str(self)

class Chords:
    __slots__ = ("_data", "groups")

    def __init__(self, data: list[ChordItem], groups: list[ChordValue]):
        self._data = data
        self.groups = groups

    def __len__(self):
        return len(self._data)

    def __iter__(self) -> Iterator[ChordItem]:
        return iter(self._data)

    def __getitem__(self, index: int) -> ChordItem:
        return self._data[index]

    def sort(self, *, key=None, reverse: bool = False):
        self._data.sort(key=key, reverse=reverse)


def compare_value(
    compare: Callable[[float, float], float],
) -> Callable[[ChordValue, ChordValue], float]:
    def local_compare(a: ChordValue, b: ChordValue):
        return compare(
            a.source.value + a.source.value,
            b.source.value + b.source.value,
        )


class Chord:
    """
    Chord layout

    Parameters
    ----------
    directed : bool
        :code:`True` for directed flow
    transpose : bool
        :code:`True` to transpose the specified matrix
    """
    def __init__(self, directed: bool, transpose: bool):
        self._directed = directed
        self._transpose = transpose
        self._pad_angle = 0
        self._sort_groups = None
        self._sort_subgroups = None
        self._sort_chords = None

    def __call__(self, matrix: list[list[float]]) -> Chords:
        """
        Computes the chord layout for the specified square matrix of size
        :math:`n \\times n`, where the matrix represents the directed flow
        amongst a network (a complete digraph) of n nodes.

        The return value of chord(matrix) is an array of chords, where each
        chord represents the combined bidirectional flow between two nodes i
        and j (where i may be equal to j) and is an object with the following
        properties:

        * :code:`source` - the source subgroup
        * :code:`target` - the target subgroup

        Each source and target subgroup is also an object with the following
        properties:

        * :code:`index` - the node index i
        * :code:`start_angle` - the start angle in radians
        * :code:`end_angle` - the end angle in radians
        * :code:`value` - the flow value matrix[i][j]

        The chords are typically passed to ribbon to display the network
        relationships.

        The returned array includes only chord objects for which the value
        :code:`matrix[i][j]` or :code:`matrix[j][i]` is non-zero. Furthermore,
        the returned array only contains unique chords: a given chord ij
        represents the bidirectional flow from i to j and from j to i, and does
        not contain a duplicate chord ji; i and j are chosen such that the
        chord's source always represents the larger of :code:`matrix[i][j]` and
        :code:`matrix[j][i]`.

        The chords array also defines a secondary array of length n,
        chords.groups, where each group represents the combined outflow for
        node i, corresponding to the elements :code:`matrix[i][0 ... n - 1]`,
        and is an object with the following properties:

        * :code:`index` - the node index i
        * :code:`start_angle` - the start angle in radians
        * :code:`end_angle` - the end angle in radians
        * :code:`value` - the total outgoing flow value for node i

        The groups are typically passed to arc to produce a donut chart around
        the circumference of the chord layout.

        Parameters
        ----------
        matrix : list[list[float]]
            Square matrix of size :math:`n \\times n`

        Returns
        -------
        Chords
            Chords Object which behaves like a list and has
            :code:`Chords.groups` attribute. Groups are typically passed to arc
            to produce a donut chart around the circumference of the chord
            layout.
        """
        n = len(matrix)
        group_sums = [None] * n
        group_index = list(range(n))
        chords = [None] * (n * n)
        groups = [None] * n
        k = 0

        matrix = (
            [matrix[i % n][i // n] for i in range(n * n)]
            if self._transpose
            else [matrix[i // n][i % n] for i in range(n * n)]
        )

        for i in range(n):
            x = 0
            for j in range(n):
                x += matrix[i * n + j] + self._directed * matrix[j * n + i]
            group_sums[i] = x
            k += x
        k = max(0, TAU - self._pad_angle * n) / k
        dx = self._pad_angle if k else TAU / n

        x = 0
        if self._sort_groups:
            group_index.sort(
                key=cmp_to_key(
                    lambda a, b: self._sort_groups(group_sums[a], group_sums[b])
                )
            )
        for i in group_index:
            x0 = x
            if self._directed:
                subgroup_index = list(
                    filter(
                        lambda j: (matrix[-j * n + i] if j < 0 else matrix[i * n + j]),
                        range(-n + 1, n),
                    )
                )
                if self._sort_subgroups:
                    subgroup_index.sort(
                        key=cmp_to_key(
                            lambda a, b: self._sort_subgroups(
                                (-matrix[-a * n + i] if a < 0 else matrix[i * n + a]),
                                (-matrix[-b * n + i] if b < 0 else matrix[i * n + b]),
                            )
                        )
                    )
                for j in subgroup_index:
                    if j < 0:
                        chord = chords[-j * n + i]
                        if chord is None:
                            chord = chords[-j * n + i] = ChordItem()
                        x_ = x
                        x += matrix[-j * n + i] * k
                        chord.target = ChordValue(i, x_, x, matrix[-j * n + i])
                    else:
                        chord = chords[i * n + j]
                        if chord is None:
                            chord = chords[i * n + j] = ChordItem()
                        x_ = x
                        x += matrix[i * n + j] * k
                        chord.source = ChordValue(i, x_, x, matrix[i * n + j])
                groups[i] = ChordValue(i, x0, x, group_sums[i])
            else:
                subgroup_index = list(
                    filter(
                        lambda j: matrix[i * n + j] or matrix[j * n + i], range(n)
                    )
                )
                if self._sort_subgroups:
                    subgroup_index.sort(
                        key=cmp_to_key(
                            lambda a, b: self._sort_subgroups(
                                matrix[i * n + a], matrix[i * n + b]
                            )
                        )
                    )
                for j in subgroup_index:
                    if i < j:
                        chord = chords[i * n + j]
                        if chord is None:
                            chord = chords[i * n + j] = ChordItem()
                        x_ = x
                        x += matrix[i * n + j] * k
                        chord.source = ChordValue(i, x_, x, matrix[i * n + j])
                    else:
                        chord = chords[j * n + i]
                        if chord is None:
                            chord = chords[j * n + i] = ChordItem()
                        x_ = x
                        x += matrix[i * n + j] * k
                        chord.target = ChordValue(i, x_, x, matrix[i * n + j])
                        if i == j:
                            chord.source = chord.target
                    if (
                        chord.source
                        and chord.target
                        and chord.source.value < chord.target.value
                    ):
                        chord.source, chord.target = chord.target, chord.source
                groups[i] = ChordValue(i, x0, x, group_sums[i])
            x += dx

        idx = 0
        while idx < len(chords):
            if chords[idx] is None:
                chords.pop(idx)
            else:
                idx += 1
        chords = Chords(chords, groups)
        if self._sort_chords:
            chords.sort(key=cmp_to_key(self._sort_chords))
        return chords

    def set_pad_angle(self, pad_angle: float) -> TChord:
        """
        Sets the pad angle between adjacent groups to the specified number in
        radians and returns this chord layout.

        Parameters
        ----------
        pad_angle : float
            Pad angle value

        Returns
        -------
        TChord
            Itself
        """
        self._pad_angle = max(0, pad_angle)
        return self

    def set_sort_groups(self, sort_groups: Callable[[float, float], float] | None = None) -> TChord:
        """
        Sets the group comparator to the specified function or :code:`None` and
        returns this chord layout.

        Parameters
        ----------
        sort_groups : Callable[[float, float], float] | None
            Sort group function

        Returns
        -------
        TChord
            Itself
        """
        self._sort_groups = sort_groups
        return self

    def set_sort_subgroups(
        self, sort_subgroups: Callable[[float, float], float] | None = None
    ) -> TChord:
        """
        Sets the subgroup comparator to the specified function or :code:`None`
        and returns this chord layout.

        Parameters
        ----------
        sort_subgroups : Callable[[float, float], float] | None
            Sort subgroups function

        Returns
        -------
        TChord
            Itself
        """
        self._sort_subgroups = sort_subgroups
        return self

    def set_sort_chords(
        self, compare: Callable[[float, float], float] | None = None
    ) -> TChord:
        """
        Sets the chord comparator to the specified function or :code:`None` and
        returns this chord layout.

        Parameters
        ----------
        compare : Callable[[float, float], float] | None
            Compare function

        Returns
        -------
        TChord
            Itself
        """
        if compare is None:
            self._sort_chords = None
        else:
            self._sort_chords = compare_value(compare)
        return self

    def get_pad_angle(self) -> float:
        return self._pad_angle

    def get_sort_groups(self) -> Callable[[float, float], float]:
        return self._sort_groups

    def get_sort_subgroups(self) -> Callable[[float, float], float]:
        return self._sort_subgroups

    def get_sort_chords(self) -> Callable[[ChordItem, ChordItem], float]:
        return self._sort_chords


def chord() -> Chord:
    """
    Constructs a new chord layout with the default settings.

    Returns
    -------
    Chord
        Chord object
    """
    return Chord(False, False)


def chord_transpose() -> Chord:
    """
    A transposed chord layout. Useful to highlight outgoing (rather than
    incoming) flows.

    Returns
    -------
    Chord
        Chord object
    """
    return Chord(False, True)


def chord_directed() -> Chord:
    """
    A chord layout for unidirectional flows. The chord from i to j is generated
    from the value in :code:`matrix[i][j]` only.

    Returns
    -------
    Chord
        Chord object
    """
    return Chord(True, False)
