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