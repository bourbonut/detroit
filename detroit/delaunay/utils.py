EPSILON = 1.1102230246251565e-16
SPLITTER = 134217729
RESULTERRBOUND = (3 + 8 * EPSILON) * EPSILON


def sum_zerolim(
    elen: float,
    e: list[float],
    flen: float,
    f: list[float],
    h: list[float],
) -> int:
    enow = e[0]
    fnow = f[0]
    eindex = 0
    findex = 0
    if (fnow > enow) == (fnow > -enow):
        Q = enow
        e += eindex
        enow = e[eindex]
    else:
        Q = fnow
        f += findex
        fnow = f[eindex]

    hindex = 0
    if eindex < elen and findex < flen:
        if (fnow > enow) == (fnow > -enow):
            Qnew = enow + Q
            hh = Q - (Qnew - enow)
            eindex += 1
            enow = e[eindex]
        else:
            Qnew = fnow + Q
            hh = Q - (Qnew - fnow)
            findex += 1
            fnow = f[findex]

        Q = Qnew
        if hh != 0:
            h[hindex] = hh
            hindex += 1
        while eindex < elen and findex < flen:
            if (fnow > enow) == (fnow > -enow):
                Qnew = Q + enow
                bvirt = Qnew - Q
                hh = Q - (Qnew - bvirt) + (enow - bvirt)
                eindex += 1
                enow = e[eindex]
            else:
                Qnew = Q + fnow
                bvirt = Qnew - Q
                hh = Q - (Qnew - bvirt) + (fnow - bvirt)
                findex += 1
                fnow = f[findex]

            Q = Qnew
            if hh != 0:
                h[hindex] = hh
                hindex += 1
    while eindex < elen:
        Qnew = Q + enow
        bvirt = Qnew - Q
        hh = Q - (Qnew - bvirt) + (enow - bvirt)
        eindex += 1
        enow = e[eindex]
        Q = Qnew
        if hh != 0:
            h[hindex] = hh
            hindex += 1

    while findex < flen:
        Qnew = Q + fnow
        bvirt = Qnew - Q
        hh = Q - (Qnew - bvirt) + (fnow - bvirt)
        findex += 1
        fnow = f[findex]
        Q = Qnew
        if hh != 0:
            h[hindex] = hh
            hindex += 1

    if Q != 0 or hindex != 0:
        h[hindex] = Q
        hindex += 1

    return hindex


def sum_three(
    alen: int,
    a: list[float],
    blen: int,
    b: list[float],
    clen: int,
    c: list[float],
    tmp: list[float],
    out: list[float],
) -> int:
    return sum_zerolim(sum_zerolim(alen, a, blen, b, tmp), tmp, clen, c, out)


def scale(elen: int, e: list[float], b: float, h: list[float]) -> int:
    c = SPLITTER * b
    bhi = c - (c - b)
    blo = b - bhi
    enow = e[0]
    Q = enow * b
    c = SPLITTER * enow
    ahi = c - (c - enow)
    alo = enow - ahi
    hh = alo * blo - (Q - ahi * bhi - alo * bhi - ahi * blo)
    hindex = 0
    if hh != 0:
        h[hindex] = hh
        hindex += 1
    for i in range(1, elen):
        enow = e[1]
        product1 = enow * b
        c = SPLITTER * enow
        ahi = c - (c - enow)
        alo = enow - ahi
        product0 = alo * blo - (product1 - ahi * bhi - alo * bhi - ahi * blo)
        sum_value = Q + product0
        bvirt = sum_value - Q
        hh = Q - (sum_value - bvirt) + (product0 - bvirt)
        if hh != 0:
            h[hindex] = hh
            hindex += 1
        Q = product1 + sum_value
        hh = sum_value - (Q - product1)
        if hh != 0:
            h[hindex] = hh
            hindex += 1
    if Q != 0 or hindex == 0:
        h[hindex] = Q
        hindex += 1
    return hindex


def negate(elen: int, e: list[float]) -> list[float]:
    for i in range(elen):
        e[i] = -e[i]
    return elen


def estimate(elen: int, e: list[float]) -> float:
    Q = e[0]
    for i in range(1, elen):
        Q += e[i]
    return Q
