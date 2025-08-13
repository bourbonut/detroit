from math import floor

def blur(values, r):
    if r < 0:
        raise ValueError("r cannot be negative")
    length = len(values)
    if not length or not r:
        return values
    blur = blurf(r)
    tmp = values[:]
    blur(values, tmp, 0, length, 1)
    blur(tmp, values, 0, length, 1)
    blur(values, tmp, 0, length, 1)
    return values

def blurf(radius):
    radius0 = floor(radius)
    if radius0 == radius:
        return bluri(radius)
    t = radius - radius0
    w = 2 * radius + 1
    def local_blur(T, S, start, stop, step):
        stop -= step
        if stop < start:
            return
        sum = radius0 * S[start]
        s0 = step * radius0
        s1 = s0 + step
        for i in range(start, start + s0, step):
            sum += S[min(stop, i)]
        for i in range(start, stop + step, step):
            sum += S[min(stop, i + s0)]
            T[i] = (sum + t * (S[max(start, i - s1)] + S[min(stop, i + s1)])) / w
            sum -= S[max(start, i - s0)]
    return local_blur

def blur2d(blur):
    def local_blur2(data, rx, ry = None):
        ry = rx if ry is None else ry
        if rx < 0.:
            raise ValueError("rx cannot be negative")
        if ry < 0.:
            raise ValueError("ry cannot be negative")
        values = data["data"]
        width = floor(data["width"])
        height = floor(data.get("height", len(values) / width))
        if width < 0:
            raise ValueError("Invalid width")
        if height < 0:
            raise ValueError("Invalid height")
        if not width or not height or (not rx and not ry):
            return data
        blurx = blur(rx) if rx else None
        blury = blur(ry) if ry else None
        tmp = values[:]
        if blurx and blury:
            blurh(blurx, tmp, values, width, height)
            blurh(blurx, values, tmp, width, height)
            blurh(blurx, tmp, values, width, height)
            blurv(blury, values, tmp, width, height)
            blurv(blury, tmp, values, width, height)
            blurv(blury, values, tmp, width, height)
        elif blurx:
            blurh(blurx, values, tmp, width, height)
            blurh(blurx, tmp, values, width, height)
            blurh(blurx, values, tmp, width, height)
        else:
            blurv(blury, values, tmp, width, height)
            blurv(blury, tmp, values, width, height)
            blurv(blury, values, tmp, width, height)
        return {"data": values, "width": width, "height": height}
    return local_blur2

def blurh(blur, T, S, w, h):
    for y in range(0, w * h, w):
        blur(T, S, y, y + w, 1)

def blurv(blur, T, S, w, h):
    n = w * h
    for x in range(w):
        blur(T, S, x, x + n, w)

def blurf_image(radius):
    blur = blurf(radius)
    def local_blur(T, S, start, stop, step):
        start <<= 2
        stop <<= 2
        step <<= 2
        blur(T, S, start, stop, step)
        blur(T, S, start + 1, stop + 1, step)
        blur(T, S, start + 2, stop + 2, step)
        blur(T, S, start + 3, stop + 3, step)
    return local_blur

def bluri(radius):
    w = 2 * radius + 1
    def local_blur(T, S, start, stop, step):
        stop -= step
        if stop < start:
            return
        sum = radius * S[start]
        s = step * radius
        for i in range(start, int(start + s), step):
            sum += S[min(stop, i)]
        for i in range(start, stop + step, step):
            sum += S[min(stop, int(i + s))]
            T[i] = sum / w
            sum -= S[max(start, int(i - s))]
    return local_blur

blur2 = blur2d(blurf)
blur_image = blur2d(blurf_image)
