def offset_diverging(series, order):
    n = len(series)
    if n == 0:
        return
    m = len(series[order[0]])
    for j in range(m):
        yp = yn = 0.0
        for i in range(n):
            d = series[order[i]][j]
            dy = d[1] - d[0]
            if dy > 0:
                d[0] = yp
                yp += dy
                d[1] = yp
            elif dy < 0:
                d[1] = yn
                yn += dy
                d[0] = yn
            else:
                d[0] = 0
                d[1] = dy
