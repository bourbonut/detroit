import detroit as d3
from detroit.chord.chord import ChordItem, ChordValue

# From http://mkweb.bcgsc.ca/circos/guide/tables/
matrix = [
    [11975, 5871, 8916, 2868],
    [1951, 10048, 2060, 6171],
    [8010, 16145, 8090, 8045],
    [1013, 990, 940, 6907],
]


def in_delta(actual, expected, delta=1e-6):
    if isinstance(expected, list):
        n = len(expected)
        if len(actual) != n:
            return False
        for i in range(n):
            if not in_delta(actual[i], expected[i], delta):
                return False
        return True
    elif isinstance(expected, ChordItem):
        source = in_delta(actual.source, expected.source, delta)
        target = in_delta(actual.target, expected.target, delta)
        return source and target
    elif isinstance(expected, ChordValue):
        index = in_delta(actual.index, expected.index, delta)
        start_angle = in_delta(actual.start_angle, expected.start_angle, delta)
        end_angle = in_delta(actual.end_angle, expected.end_angle, delta)
        value = in_delta(actual.value, expected.value, delta)
        return index and start_angle and end_angle and value
    else:
        return actual >= expected - delta and actual <= expected + delta


def test_chord_1():
    c = d3.chord()
    assert c.get_pad_angle() == 0
    assert c.get_sort_groups() is None
    assert c.get_sort_subgroups() is None
    assert c.get_sort_chords() is None
    chords = c(matrix)
    assert in_delta(
        chords.groups,
        [
            ChordValue(0, 0.0000000, 1.8617078, 29630),
            ChordValue(1, 1.8617078, 3.1327961, 20230),
            ChordValue(2, 3.1327961, 5.6642915, 40290),
            ChordValue(3, 5.6642915, 6.2831853, 9850),
        ],
    )
    assert in_delta(
        chords._data,
        [
            ChordItem(
                ChordValue(0, 0.0000000, 0.7524114, 11975),
                ChordValue(0, 0.0000000, 0.7524114, 11975),
            ),
            ChordItem(
                ChordValue(0, 0.7524114, 1.1212972, 5871),
                ChordValue(1, 1.8617078, 1.9842927, 1951),
            ),
            ChordItem(
                ChordValue(0, 1.1212972, 1.6815060, 8916),
                ChordValue(2, 3.1327961, 3.6360793, 8010),
            ),
            ChordItem(
                ChordValue(0, 1.6815060, 1.8617078, 2868),
                ChordValue(3, 5.6642915, 5.7279402, 1013),
            ),
            ChordItem(
                ChordValue(1, 1.9842927, 2.6156272, 10048),
                ChordValue(1, 1.9842927, 2.6156272, 10048),
            ),
            ChordItem(
                ChordValue(2, 3.6360793, 4.6504996, 16145),
                ChordValue(1, 2.6156272, 2.7450608, 2060),
            ),
            ChordItem(
                ChordValue(1, 2.7450608, 3.1327961, 6171),
                ChordValue(3, 5.7279402, 5.7901437, 990),
            ),
            ChordItem(
                ChordValue(2, 4.6504996, 5.1588092, 8090),
                ChordValue(2, 4.6504996, 5.1588092, 8090),
            ),
            ChordItem(
                ChordValue(2, 5.1588092, 5.6642915, 8045),
                ChordValue(3, 5.7901437, 5.8492056, 940),
            ),
            ChordItem(
                ChordValue(3, 5.8492056, 6.2831853, 6907),
                ChordValue(3, 5.8492056, 6.2831853, 6907),
            ),
        ],
    )


def test_chord_2():
    c = d3.chord().set_sort_subgroups(lambda a, b: b - a)
    assert c.set_pad_angle(0.05) == c
    assert c.get_pad_angle() == 0.05
    chords = c(matrix)
    assert in_delta(
        chords.groups,
        [
            ChordValue(0, 0.0000000, 1.80244780, 29630),
            ChordValue(1, 1.8524478, 3.08307619, 20230),
            ChordValue(2, 3.1330761, 5.58399155, 40290),
            ChordValue(3, 5.6339915, 6.23318530, 9850),
        ],
    )
    assert in_delta(
        chords._data,
        [
            ChordItem(
                ChordValue(0, 0.0000000, 0.7284614, 11975),
                ChordValue(0, 0.0000000, 0.7284614, 11975),
            ),
            ChordItem(
                ChordValue(0, 1.2708382, 1.6279820, 5871),
                ChordValue(1, 2.9643932, 3.0830761, 1951),
            ),
            ChordItem(
                ChordValue(0, 0.7284614, 1.2708382, 8916),
                ChordValue(2, 5.0967284, 5.5839915, 8010),
            ),
            ChordItem(
                ChordValue(0, 1.6279820, 1.8024478, 2868),
                ChordValue(3, 6.0541571, 6.1157798, 1013),
            ),
            ChordItem(
                ChordValue(1, 1.8524478, 2.4636862, 10048),
                ChordValue(1, 1.8524478, 2.4636862, 10048),
            ),
            ChordItem(
                ChordValue(2, 3.1330761, 4.1152064, 16145),
                ChordValue(1, 2.8390796, 2.9643932, 2060),
            ),
            ChordItem(
                ChordValue(1, 2.4636862, 2.8390796, 6171),
                ChordValue(3, 6.1157798, 6.1760033, 990),
            ),
            ChordItem(
                ChordValue(2, 4.1152064, 4.6073361, 8090),
                ChordValue(2, 4.1152064, 4.6073361, 8090),
            ),
            ChordItem(
                ChordValue(2, 4.6073361, 5.0967284, 8045),
                ChordValue(3, 6.1760033, 6.2331853, 940),
            ),
            ChordItem(
                ChordValue(3, 5.6339915, 6.0541571, 6907),
                ChordValue(3, 5.6339915, 6.0541571, 6907),
            ),
        ],
    )
