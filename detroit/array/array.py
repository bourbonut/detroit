# src/disjoint.py
from internmap import InternSet

def disjoint(values, other):
    iterator = iter(other)
    set_ = InternSet()
    for v in values:
        if v in set_:
            return False
        for value in iterator:
            if value is None:
                break
            if v is value:
                return False
            set_.add(value)
    return True

# ----- 

# src/minIndex.py
def min_index(values, valueof=None):
    min_value = None
    min_index = -1
    index = -1
    if valueof is None:
        for value in values:
            index += 1
            if value is not None and (min_value > value or (min_value is None and value >= value)):
                min_value, min_index = value, index
    else:
        for value in values:
            index += 1
            value = valueof(value, index, values)
            if value is not None and (min_value > value or (min_value is None and value >= value)):
                min_value, min_index = value, index
    return min_index

# ----- 

# src/bisect.py
from .ascending import ascending
from .bisector import bisector
from .number import number

ascending_bisect = bisector(ascending)
bisect_right = ascending_bisect['right']
bisect_left = ascending_bisect['left']
bisect_center = bisector(number)['center']

# ----- 

# src/leastIndex.py
from .ascending import ascending
from .minIndex import min_index

def least_index(values, compare=ascending):
    if len(inspect.signature(compare).parameters) == 1:
        return min_index(values, compare)
    min_value = None
    min_idx = -1
    index = -1
    for value in values:
        index += 1
        if min_idx < 0:
            if compare(value, value) == 0:
                min_value = value
                min_idx = index
        else:
            if compare(value, min_value) < 0:
                min_value = value
                min_idx = index
    return min_idx

# ----- 

# src/ticks.py
import math

e10 = math.sqrt(50)
e5 = math.sqrt(10)
e2 = math.sqrt(2)

def tick_spec(start, stop, count):
    step = (stop - start) / max(0, count)
    power = math.floor(math.log10(step))
    error = step / (10 ** power)
    factor = 10 if error >= e10 else 5 if error >= e5 else 2 if error >= e2 else 1
    if power < 0:
        inc = (10 ** -power) / factor
        i1 = round(start * inc)
        i2 = round(stop * inc)
        if i1 / inc < start:
            i1 += 1
        if i2 / inc > stop:
            i2 -= 1
        inc = -inc
    else:
        inc = (10 ** power) * factor
        i1 = round(start / inc)
        i2 = round(stop / inc)
        if i1 * inc < start:
            i1 += 1
        if i2 * inc > stop:
            i2 -= 1
    if i2 < i1 and 0.5 <= count < 2:
        return tick_spec(start, stop, count * 2)
    return [i1, i2, inc]

def ticks(start, stop, count):
    stop = float(stop)
    start = float(start)
    count = float(count)
    if count <= 0:
        return []
    if start == stop:
        return [start]
    reverse = stop < start
    i1, i2, inc = (tick_spec(stop, start, count) if reverse else tick_spec(start, stop, count))
    if i2 < i1:
        return []
    n = i2 - i1 + 1
    tick_list = [0] * n
    if reverse:
        if inc < 0:
            for i in range(n):
                tick_list[i] = (i2 - i) / -inc
        else:
            for i in range(n):
                tick_list[i] = (i2 - i) * inc
    else:
        if inc < 0:
            for i in range(n):
                tick_list[i] = (i1 + i) / -inc
        else:
            for i in range(n):
                tick_list[i] = (i1 + i) * inc
    return tick_list

def tick_increment(start, stop, count):
    stop = float(stop)
    start = float(start)
    count = float(count)
    return tick_spec(start, stop, count)[2]

def tick_step(start, stop, count):
    stop = float(stop)
    start = float(start)
    count = float(count)
    reverse = stop < start
    inc = tick_increment(stop, start, count) if reverse else tick_increment(start, stop, count)
    return (1 if not reverse else -1) * (1 / -inc if inc < 0 else inc)

# ----- 

# src/cumsum.py
import numpy as np

def cumsum(values, valueof=None):
    sum_ = 0
    index = 0
    return np.fromiter((sum_ := sum_ + (valueof(v, index, values) if valueof else (sum_ + v if v is not None else 0)) for index, v in enumerate(values)), dtype=float)

# ----- 

# src/some.py
def some(values, test):
    if not callable(test):
        raise TypeError("test is not a function")
    index = -1
    for value in values:
        index += 1
        if test(value, index, values):
            return True
    return False

# ----- 

# src/reduce.py
def reduce(values, reducer, value=None):
    if not callable(reducer):
        raise TypeError("reducer is not a function")
    iterator = iter(values)
    done = False
    index = -1
    if value is None:
        try:
            value = next(iterator)
            index += 1
        except StopIteration:
            return
    for next_value in iterator:
        value = reducer(value, next_value, index, values)
        index += 1
    return value

# ----- 

# src/greatestIndex.py
from .ascending import ascending
from .maxIndex import max_index

def greatest_index(values, compare=ascending):
    if len(inspect.signature(compare).parameters) == 1:
        return max_index(values, compare)
    max_value = None
    max_idx = -1
    index = -1
    for value in values:
        index += 1
        if max_idx < 0:
            if compare(value, value) == 0:
                max_value = value
                max_idx = index
        else:
            if compare(value, max_value) > 0:
                max_value = value
                max_idx = index
    return max_idx

# ----- 

# src/sum.py
def sum_(values, valueof=None):
    total = 0
    if valueof is None:
        for value in values:
            if (value := float(value)) is not None:
                total += value
    else:
        index = -1
        for value in values:
            if (value := float(valueof(value, index := index + 1, values))) is not None:
                total += value
    return total

# ----- 

# src/variance.py
def variance(values, valueof=None):
    count = 0
    delta = None
    mean = 0
    sum_ = 0
    if valueof is None:
        for value in values:
            if value is not None and (value := float(value)) >= value:
                delta = value - mean
                mean += delta / (count := count + 1)
                sum_ += delta * (value - mean)
    else:
        index = -1
        for value in values:
            if (value := valueof(value, index := index + 1, values)) is not None and (value := float(value)) >= value:
                delta = value - mean
                mean += delta / (count := count + 1)
                sum_ += delta * (value - mean)
    return sum_ / (count - 1) if count > 1 else None

# ----- 

# src/every.py
def every(values, test):
    if not callable(test):
        raise TypeError("test is not a function")
    index = -1
    for value in values:
        index += 1
        if not test(value, index, values):
            return False
    return True

# ----- 

# src/median.py
from .quantile import quantile, quantile_index

def median(values, valueof=None):
    return quantile(values, 0.5, valueof)

def median_index(values, valueof=None):
    return quantile_index(values, 0.5, valueof)

# ----- 

# src/number.py
def number(x):
    return float(x) if x is not None else float('nan')

def numbers(values, valueof=None):
    index = -1
    if valueof is None:
        for value in values:
            if value is not None and (value := float(value)) >= value:
                yield value
    else:
        for value in values:
            if (value := valueof(value, index := index + 1, values)) is not None and (value := float(value)) >= value:
                yield value

# ----- 

# src/bisector.py
from .ascending import ascending
from .descending import descending

def bisector(f):
    compare1, compare2, delta = None, None, None

    if len(inspect.signature(f).parameters) != 2:
        compare1 = ascending
        compare2 = lambda d, x: ascending(f(d), x)
        delta = lambda d, x: f(d) - x
    else:
        compare1 = f if f in (ascending, descending) else zero
        compare2 = f
        delta = f

    def left(a, x, lo=0, hi=None):
        if hi is None:
            hi = len(a)
        if lo < hi:
            if compare1(x, x) != 0:
                return hi
            while lo < hi:
                mid = (lo + hi) >> 1
                if compare2(a[mid], x) < 0:
                    lo = mid + 1
                else:
                    hi = mid
        return lo

    def right(a, x, lo=0, hi=None):
        if hi is None:
            hi = len(a)
        if lo < hi:
            if compare1(x, x) != 0:
                return hi
            while lo < hi:
                mid = (lo + hi) >> 1
                if compare2(a[mid], x) <= 0:
                    lo = mid + 1
                else:
                    hi = mid
        return lo

    def center(a, x, lo=0, hi=None):
        if hi is None:
            hi = len(a)
        i = left(a, x, lo, hi - 1)
        return i - 1 if i > lo and delta(a[i - 1], x) > -delta(a[i], x) else i

    return {'left': left, 'center': center, 'right': right}

def zero():
    return 0

# ----- 

# src/greatest.py
from .ascending import ascending

def greatest(values, compare=ascending):
    max_ = None
    defined = False
    if len(inspect.signature(compare).parameters) == 1:
        max_value = None
        for element in values:
            value = compare(element)
            if defined:
                if ascending(value, max_value) > 0:
                    max_, max_value = element, value
            else:
                if ascending(value, value) == 0:
                    max_, max_value = element, value
                    defined = True
    else:
        for value in values:
            if defined:
                if compare(value, max_) > 0:
                    max_ = value
            else:
                if compare(value, value) == 0:
                    max_ = value
                    defined = True
    return max_

# ----- 

# src/bin.py
from .array import slice
from .bisect import bisect
from .constant import constant
from .extent import extent
from .identity import identity
from .nice import nice
from .ticks import ticks, tick_increment
from .threshold.sturges import sturges

def bin():
    value = identity
    domain = extent
    threshold = sturges

    def histogram(data):
        if not isinstance(data, list):
            data = list(data)

        n = len(data)
        values = [0] * n

        for i in range(n):
            values[i] = value(data[i], i, data)

        xz = domain(values)
        x0, x1 = xz[0], xz[1]
        tz = threshold(values, x0, x1)

        if not isinstance(tz, list):
            max_ = x1
            tn = int(tz)
            if domain == extent:
                x0, x1 = nice(x0, x1, tn)
            tz = ticks(x0, x1, tn)

            if tz[0] <= x0:
                step = tick_increment(x0, x1, tn)

            if tz[-1] >= x1:
                if max_ >= x1 and domain == extent:
                    step = tick_increment(x0, x1, tn)
                    if step.is_finite():
                        if step > 0:
                            x1 = (math.floor(x1 / step) + 1) * step
                        elif step < 0:
                            x1 = (math.ceil(x1 * -step) + 1) / -step
                else:
                    tz.pop()

        m = len(tz)
        a = 0
        b = m
        while tz[a] <= x0:
            a += 1
        while tz[b - 1] > x1:
            b -= 1
        if a or b < m:
            tz = tz[a:b]
            m = b - a

        bins = [None] * (m + 1)

        for i in range(m + 1):
            bin_ = bins[i] = []
            bin_.x0 = tz[i - 1] if i > 0 else x0
            bin_.x1 = tz[i] if i < m else x1

        if step.is_finite():
            if step > 0:
                for i in range(n):
                    if (x := values[i]) is not None and x0 <= x <= x1:
                        bins[min(m, math.floor((x - x0) / step))].append(data[i])
            elif step < 0:
                for i in range(n):
                    if (x := values[i]) is not None and x0 <= x <= x1:
                        j = math.floor((x0 - x) * step)
                        bins[min(m, j + (tz[j] <= x))].append(data[i])
        else:
            for i in range(n):
                if (x := values[i]) is not None and x0 <= x <= x1:
                    bins[bisect(tz, x, 0, m)].append(data[i])

        return bins

    histogram.value = lambda _: (value := _ if _ is not None else value, histogram) if _ is not None else value
    histogram.domain = lambda _: (domain := _ if _ is not None else constant([_[0], _[1]]), histogram) if _ is not None else domain
    histogram.thresholds = lambda _: (threshold := _ if _ is not None else constant(list(slice(_))), histogram) if _ is not None else threshold

    return histogram

# ----- 

# src/scan.py
from .leastIndex import least_index

def scan(values, compare):
    index = least_index(values, compare)
    return None if index < 0 else index

# ----- 

# src/least.py
from .ascending import ascending

def least(values, compare=ascending):
    min_ = None
    defined = False
    if len(inspect.signature(compare).parameters) == 1:
        min_value = None
        for element in values:
            value = compare(element)
            if defined:
                if ascending(value, min_value) < 0:
                    min_, min_value = element, value
            else:
                if ascending(value, value) == 0:
                    min_, min_value = element, value
                    defined = True
    else:
        for value in values:
            if defined:
                if compare(value, min_) < 0:
                    min_ = value
            else:
                if compare(value, value) == 0:
                    min_ = value
                    defined = True
    return min_

# ----- 

# src/quickselect.py
from .sort import ascending_defined, compare_defined

def quickselect(array, k, left=0, right=float('inf'), compare=None):
    k = math.floor(k)
    left = math.floor(max(0, left))
    right = math.floor(min(len(array) - 1, right))

    if not (left <= k <= right):
        return array

    compare = ascending_defined if compare is None else compare_defined(compare)

    while right > left:
        if right - left > 600:
            n = right - left + 1
            m = k - left + 1
            z = math.log(n)
            s = 0.5 * math.exp(2 * z / 3)
            sd = 0.5 * math.sqrt(z * s * (n - s) / n) * (-1 if m - n / 2 < 0 else 1)
            new_left = max(left, math.floor(k - m * s / n + sd))
            new_right = min(right, math.floor(k + (n - m) * s / n + sd))
            quickselect(array, k, new_left, new_right, compare)

        t = array[k]
        i = left
        j = right

        swap(array, left, k)
        if compare(array[right], t) > 0:
            swap(array, left, right)

        while i < j:
            swap(array, i, j)
            i += 1
            j -= 1
            while compare(array[i], t) < 0:
                i += 1
            while compare(array[j], t) > 0:
                j -= 1

        if compare(array[left], t) == 0:
            swap(array, left, j)
        else:
            j += 1
            swap(array, j, right)

        if j <= k:
            left = j + 1
        if k <= j:
            right = j - 1

    return array

def swap(array, i, j):
    array[i], array[j] = array[j], array[i]

# ----- 

# src/maxIndex.py
def max_index(values, valueof=None):
    max_ = None
    max_index = -1
    index = -1
    if valueof is None:
        for value in values:
            index += 1
            if value is not None and (max_ < value or (max_ is None and value >= value)):
                max_, max_index = value, index
    else:
        for value in values:
            index += 1
            value = valueof(value, index, values)
            if value is not None and (max_ < value or (max_ is None and value >= value)):
                max_, max_index = value, index
    return max_index

# ----- 

# src/nice.py
from .ticks import tick_increment

def nice(start, stop, count):
    prestep = None
    while True:
        step = tick_increment(start, stop, count)
        if step == prestep or step == 0 or not math.isfinite(step):
            return [start, stop]
        elif step > 0:
            start = math.floor(start / step) * step
            stop = math.ceil(stop / step) * step
        elif step < 0:
            start = math.ceil(start * step) / step
            stop = math.floor(stop * step) / step
        prestep = step

# ----- 

# src/range.py
def range_(start, stop=None, step=None):
    if stop is None:
        stop = start
        start = 0
        step = 1
    elif step is None:
        step = 1

    start = float(start)
    stop = float(stop)
    step = float(step)

    n = max(0, math.ceil((stop - start) / step)) | 0
    return [start + i * step for i in range(n)]

# ----- 

# src/groupSort.py
from .ascending import ascending
from .group import group, rollup
from .sort import sort

def group_sort(values, reduce, key):
    return (sort(rollup(values, reduce, key), key=lambda x: (ascending(x[1], x[1]), ascending(x[0], x[0]))) if len(inspect.signature(reduce).parameters) != 2 else sort(group(values, key), key=lambda x: (reduce(x[1], x[1]), ascending(x[0], x[0]))))

# ----- 

# src/descending.py
def descending(a, b):
    return float('nan') if a is None or b is None else (-1 if b < a else (1 if b > a else (0 if b >= a else float('nan'))))

# ----- 

# src/cross.py
def length(array):
    return len(array) | 0

def empty(length):
    return not (length > 0)

def arrayify(values):
    return values if isinstance(values, (list, tuple)) else list(values)

def reducer(reduce):
    return lambda values: reduce(*values)

def cross(*values):
    reduce = reducer(values.pop()) if callable(values[-1]) else None
    values = [arrayify(v) for v in values]
    lengths = [length(v) for v in values]
    j = len(values) - 1
    index = [0] * (j + 1)
    product = []
    if j < 0 or any(empty(l) for l in lengths):
        return product
    while True:
        product.append([values[i][index[i]] for i in range(j + 1)])
        i = j
        while index[i] + 1 == lengths[i]:
            if i == 0:
                return [reduce(p) for p in product] if reduce else product
            index[i] = 0
            i -= 1
        index[i] += 1

# ----- 

# src/transpose.py
from .min import min_

def transpose(matrix):
    if not (n := len(matrix)):
        return []
    m = min_(matrix, length)
    transpose = [[None] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            transpose[i][j] = matrix[j][i]
    return transpose

def length(d):
    return len(d)

# ----- 

# src/blur.py
def blur(values, r):
    r = float(r)
    if r < 0:
        raise ValueError("invalid r")
    length = len(values)
    length = int(length)
    if length < 0:
        raise ValueError("invalid length")
    if not length or not r:
        return values
    blur_func = blurf(r)
    temp = values[:]
    blur_func(values, temp, 0, length, 1)
    blur_func(temp, values, 0, length, 1)
    blur_func(values, temp, 0, length, 1)
    return values

def blur2(blur):
    return lambda data, rx, ry=None: None

def blur_image(radius):
    blur = blurf(radius)
    return lambda T, S, start, stop, step: None

def blurf(radius):
    radius0 = int(radius)
    if radius0 == radius:
        return bluri(radius)
    t = radius - radius0
    w = 2 * radius + 1
    return lambda T, S, start, stop, step: None

def bluri(radius):
    w = 2 * radius + 1
    return lambda T, S, start, stop, step: None

# ----- 

# src/ascending.py
def ascending(a, b):
    return float('nan') if a is None or b is None else (-1 if a < b else (1 if a > b else (0 if a >= b else float('nan'))))

# ----- 

# src/reverse.py
def reverse(values):
    if not hasattr(values, '__iter__'):
        raise TypeError("values is not iterable")
    return list(reversed(values))

# ----- 

# src/group.py
from internmap import InternMap
from .identity import identity

def group(values, *keys):
    return nest(values, identity, identity, keys)

def groups(values, *keys):
    return nest(values, list, identity, keys)

def flatten(groups, keys):
    for i in range(1, len(keys)):
        groups = [g.pop().extend((key, value) for key, value in g) for g in groups]
    return groups

def flat_group(values, *keys):
    return flatten(groups(values, *keys), keys)

def flat_rollup(values, reduce, *keys):
    return flatten(rollups(values, reduce, *keys), keys)

def rollup(values, reduce, *keys):
    return nest(values, identity, reduce, keys)

def rollups(values, reduce, *keys):
    return nest(values, list, reduce, keys)

def index(values, *keys):
    return nest(values, identity, unique, keys)

def indexes(values, *keys):
    return nest(values, list, unique, keys)

def unique(values):
    if len(values) != 1:
        raise ValueError("duplicate key")
    return values[0]

def nest(values, map_func, reduce, keys):
    def regroup(values, i):
        if i >= len(keys):
            return reduce(values)
        groups = InternMap()
        keyof = keys[i]
        index = -1
        for value in values:
            key = keyof(value, index := index + 1, values)
            group = groups.get(key)
            if group:
                group.append(value)
            else:
                groups[key] = [value]
        for key, values in groups.items():
            groups[key] = regroup(values, i + 1)
        return map_func(groups)
    return regroup(values, 0)

# ----- 

# src/quantile.py
from .max import max_
from .maxIndex import max_index
from .min import min_
from .minIndex import min_index
from .quickselect import quickselect
from .number import number
from .sort import ascending_defined
from .greatest import greatest

def quantile(values, p, valueof=None):
    values = np.array([number(v) for v in values])
    n = len(values)
    if n == 0 or math.isnan(p):
        return
    if p <= 0 or n < 2:
        return min_(values)
    if p >= 1:
        return max_(values)
    i = (n - 1) * p
    i0 = math.floor(i)
    value0 = max_(quickselect(values, i0)[:i0 + 1])
    value1 = min_(values[i0 + 1:])
    return value0 + (value1 - value0) * (i - i0)

def quantile_sorted(values, p, valueof=number):
    n = len(values)
    if n == 0 or math.isnan(p):
        return
    if p <= 0 or n < 2:
        return valueof(values[0], 0, values)
    if p >= 1:
        return valueof(values[n - 1], n - 1, values)
    i = (n - 1) * p
    i0 = math.floor(i)
    value0 = valueof(values[i0], i0, values)
    value1 = valueof(values[i0 + 1], i0 + 1, values)
    return value0 + (value1 - value0) * (i - i0)

def quantile_index(values, p, valueof=number):
    if math.isnan(p):
        return
    numbers = np.array([number(valueof(values[i], i, values)) for i in range(len(values))])
    if p <= 0:
        return min_index(numbers)
    if p >= 1:
        return max_index(numbers)
    index = np.arange(len(values), dtype=np.uint32)
    j = len(numbers) - 1
    i = math.floor(j * p)
    quickselect(index, i, 0, j, lambda i, j: ascending_defined(numbers[i], numbers[j]))
    i = greatest(index[:i + 1], lambda i: numbers[i])
    return i if i >= 0 else -1

# ----- 

# src/constant.py
def constant(x):
    return lambda: x

# ----- 

# src/zip.py
from .transpose import transpose

def zip_(*args):
    return transpose(args)

# ----- 

# src/permute.py
def permute(source, keys):
    return [source[key] for key in keys]

# ----- 

# src/min.py
def min_(values, valueof=None):
    min_ = None
    if valueof is None:
        for value in values:
            if value is not None and (min_ > value or (min_ is None and value >= value)):
                min_ = value
    else:
        index = -1
        for value in values:
            value = valueof(value, index := index + 1, values)
            if value is not None and (min_ > value or (min_ is None and value >= value)):
                min_ = value
    return min_

# ----- 

# src/mode.py
from internmap import InternMap

def mode(values, valueof=None):
    counts = InternMap()
    if valueof is None:
        for value in values:
            if value is not None and value >= value:
                counts[value] = counts.get(value, 0) + 1
    else:
        index = -1
        for value in values:
            if (value := valueof(value, index := index + 1, values)) is not None and value >= value:
                counts[value] = counts.get(value, 0) + 1
    mode_value = None
    mode_count = 0
    for value, count in counts.items():
        if count > mode_count:
            mode_count = count
            mode_value = value
    return mode_value

# ----- 

# src/extent.py
def extent(values, valueof=None):
    min_ = None
    max_ = None
    if valueof is None:
        for value in values:
            if value is not None:
                if min_ is None:
                    min_ = max_ = value
                else:
                    if min_ > value:
                        min_ = value
                    if max_ < value:
                        max_ = value
    else:
        index = -1
        for value in values:
            if (value := valueof(value, index := index + 1, values)) is not None:
                if min_ is None:
                    min_ = max_ = value
                else:
                    if min_ > value:
                        min_ = value
                    if max_ < value:
                        max_ = value
    return [min_, max_]

# ----- 

# src/union.py
from internmap import InternSet

def union(*others):
    set_ = InternSet()
    for other in others:
        for o in other:
            set_.add(o)
    return set_

# ----- 

# src/map.py
def map_(values, mapper):
    if not hasattr(values, '__iter__'):
        raise TypeError("values is not iterable")
    if not callable(mapper):
        raise TypeError("mapper is not a function")
    return [mapper(value, index, values) for index, value in enumerate(values)]

# ----- 

# src/array.py
array = list

slice = array.__getitem__
map_ = array.__iter__

# ----- 

# src/intersection.py
from internmap import InternSet

def intersection(values, *others):
    values = InternSet(values)
    others = [set_(other) for other in others]
    for value in values:
        for other in others:
            if value not in other:
                values.remove(value)
                continue
    return values

def set_(values):
    return values if isinstance(values, InternSet) else InternSet(values)

# ----- 

# src/subset.py
from .superset import superset

def subset(values, other):
    return superset(other, values)

# ----- 

# src/count.py
def count(values, valueof=None):
    count = 0
    if valueof is None:
        for value in values:
            if value is not None and (value := float(value)) >= value:
                count += 1
    else:
        index = -1
        for value in values:
            if (value := valueof(value, index := index + 1, values)) is not None and (value := float(value)) >= value:
                count += 1
    return count

# ----- 

# src/pairs.py
def pairs(values, pairof=None):
    pairs = []
    previous = None
    first = False
    for value in values:
        if first:
            pairs.append(pairof(previous, value))
        previous = value
        first = True
    return pairs

def pair(a, b):
    return [a, b]

# ----- 

# src/index.py
from .bisect import bisect, bisect_right, bisect_left, bisect_center
from .ascending import ascending
from .bisector import bisector
from .blur import blur, blur2, blur_image
from .count import count
from .cross import cross
from .cumsum import cumsum
from .descending import descending
from .deviation import deviation
from .extent import extent
from .fsum import Adder, fsum, fcumsum
from .group import group, flat_group, flat_rollup, groups, index, indexes, rollup, rollups
from .groupSort import group_sort
from .bin import bin, histogram
from .threshold.freedmanDiaconis import threshold_freedman_diaconis
from .threshold.scott import threshold_scott
from .threshold.sturges import threshold_sturges
from .max import max_
from .maxIndex import max_index
from .mean import mean
from .median import median, median_index
from .merge import merge
from .min import min_
from .minIndex import min_index
from .mode import mode
from .nice import nice
from .pairs import pairs
from .permute import permute
from .quantile import quantile, quantile_index, quantile_sorted
from .quickselect import quickselect
from .range import range_
from .rank import rank
from .least import least
from .leastIndex import least_index
from .greatest import greatest
from .greatestIndex import greatest_index
from .scan import scan
from .shuffle import shuffle, shuffler
from .sum import sum_
from .ticks import ticks, tick_increment, tick_step
from .transpose import transpose
from .variance import variance
from .zip import zip_
from .every import every
from .some import some
from .filter import filter
from .map import map_
from .reduce import reduce
from .reverse import reverse
from .sort import sort
from .difference import difference
from .disjoint import disjoint
from .intersection import intersection
from .subset import subset
from .superset import superset
from .union import union
from internmap import InternMap, InternSet

# ----- 

# src/mean.py
def mean(values, valueof=None):
    count = 0
    total = 0
    if valueof is None:
        for value in values:
            if value is not None and (value := float(value)) >= value:
                count += 1
                total += value
    else:
        index = -1
        for value in values:
            if (value := valueof(value, index := index + 1, values)) is not None and (value := float(value)) >= value:
                count += 1
                total += value
    return total / count if count else None

# ----- 

# src/sort.py
from .ascending import ascending
from .permute import permute

def sort(values, *F):
    if not hasattr(values, '__iter__'):
        raise TypeError("values is not iterable")
    values = list(values)
    f = F[0] if F else None
    if (f and len(inspect.signature(f).parameters) != 2) or len(F) > 1:
        index = np.arange(len(values), dtype=np.uint32)
        if len(F) > 1:
            F = [list(map(f, values)) for f in F]
            index.sort(key=lambda i: [ascending_defined(f[i], f[j]) for f in F])
        else:
            f = list(map(f, values))
            index.sort(key=lambda i: ascending_defined(f[i], f[j]))
        return permute(values, index)
    return sorted(values, key=f)

def compare_defined(compare=ascending):
    if compare == ascending:
        return ascending_defined
    if not callable(compare):
        raise TypeError("compare is not a function")
    return lambda a, b: (compare(b, b) == 0) - (compare(a, a) == 0) or compare(a, b)

def ascending_defined(a, b):
    return (a is None or not (a >= a)) - (b is None or not (b >= b)) or (a < b) - (a > b)

# ----- 

# src/filter.py
def filter_(values, test):
    if not callable(test):
        raise TypeError("test is not a function")
    array = []
    index = -1
    for value in values:
        index += 1
        if test(value, index, values):
            array.append(value)
    return array

# ----- 

# src/rank.py
from .ascending import ascending
from .sort import ascending_defined, compare_defined

def rank(values, valueof=ascending):
    if not hasattr(values, '__iter__'):
        raise TypeError("values is not iterable")
    V = list(values)
    R = np.zeros(len(V))
    if len(inspect.signature(valueof).parameters) != 2:
        V = list(map(valueof, V))
        valueof = ascending
    compare_index = lambda i, j: valueof(V[i], V[j])
    k, r = None, None
    values = np.arange(len(V), dtype=np.uint32)
    values.sort(key=lambda i, j: ascending_defined(V[i], V[j]) if valueof == ascending else compare_defined(compare_index))
    for j in values:
        c = compare_index(j, k if k is not None else j)
        if c >= 0:
            if k is None or c > 0:
                k, r = j, i
            R[j] = r
        else:
            R[j] = float('nan')
    return R

# ----- 

# src/superset.py
def superset(values, other):
    iterator = iter(values)
    set_ = set()
    for o in other:
        io = intern(o)
        if io in set_:
            continue
        while True:
            try:
                value = next(iterator)
            except StopIteration:
                return False
            ivalue = intern(value)
            set_.add(ivalue)
            if io is ivalue:
                break
    return True

def intern(value):
    return value.value_of() if value is not None and isinstance(value, dict) else value

# ----- 

# src/deviation.py
from .variance import variance

def deviation(values, valueof=None):
    v = variance(values, valueof)
    return math.sqrt(v) if v else v

# ----- 

# src/identity.py
def identity(x):
    return x

# ----- 

# src/difference.py
from internmap import InternSet

def difference(values, *others):
    values = InternSet(values)
    for other in others:
        for value in other:
            values.remove(value)
    return values

# ----- 

# src/max.py
def max_(values, valueof=None):
    max_ = None
    if valueof is None:
        for value in values:
            if value is not None and (max_ < value or (max_ is None and value >= value)):
                max_ = value
    else:
        index = -1
        for value in values:
            value = valueof(value, index := index + 1, values)
            if value is not None and (max_ < value or (max_ is None and value >= value)):
                max_ = value
    return max_

# ----- 

# src/merge.py
def flatten(arrays):
    for array in arrays:
        yield from array

def merge(arrays):
    return list(flatten(arrays))

# ----- 

# src/fsum.py
class Adder:
    def __init__(self):
        self._partials = np.zeros(32)
        self._n = 0

    def add(self, x):
        p = self._partials
        i = 0
        for j in range(min(self._n, 32)):
            y = p[j]
            hi = x + y
            lo = x - (hi - y) if abs(x) < abs(y) else y - (hi - x)
            if lo:
                p[i] = lo
                i += 1
            x = hi
        p[i] = x
        self._n = i + 1
        return self

    def value_of(self):
        p = self._partials
        n = self._n
        x, y, lo, hi = 0, 0, 0, 0
        if n > 0:
            hi = p[n - 1]
            while n > 0:
                x = hi
                y = p[n - 1]
                hi = x + y
                lo = y - (hi - x)
                if lo:
                    break
                n -= 1
            if n > 0 and ((lo < 0 and p[n - 1] < 0) or (lo > 0 and p[n - 1] > 0)):
                y = lo * 2
                x = hi + y
                if y == x - hi:
                    hi = x
        return hi

def fsum(values, valueof=None):
    adder = Adder()
    if valueof is None:
        for value in values:
            if (value := float(value)):
                adder.add(value)
    else:
        index = -1
        for value in values:
            if (value := float(valueof(value, index := index + 1, values))):
                adder.add(value)
    return adder.value_of()

def fcumsum(values, valueof=None):
    adder = Adder()
    index = -1
    return np.fromiter((adder.add(float(v) or 0) for index, v in enumerate(values)), dtype=float)

# ----- 

# src/shuffle.py
import random

def shuffler(random=random.random):
    def shuffle(array, i0=0, i1=None):
        if i1 is None:
            i1 = len(array)
        m = i1 - (i0 := float(i0))
        while m:
            i = int(random() * m)
            array[m + i0], array[i + i0] = array[i + i0], array[m + i0]
            m -= 1
        return array
    return shuffle

shuffler = shuffler()

# ----- 

# src/threshold/freedmanDiaconis.py
from .count import count
from .quantile import quantile

def threshold_freedman_diaconis(values, min_, max_):
    c = count(values)
    d = quantile(values, 0.75) - quantile(values, 0.25)
    return math.ceil((max_ - min_) / (2 * d * (c ** (-1 / 3)))) if c and d else 1

# ----- 

# src/threshold/scott.py
from .count import count
from .deviation import deviation

def threshold_scott(values, min_, max_):
    c = count(values)
    d = deviation(values)
    return math.ceil((max_ - min_) * (c ** (1 / 3)) / (3.49 * d)) if c and d else 1

# ----- 

# src/threshold/sturges.py
from .count import count

def threshold_sturges(values):
    return max(1, math.ceil(math.log(count(values)) / math.log(2)) + 1)

# -----
