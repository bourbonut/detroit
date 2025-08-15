def area(ring):
    i = 0
    n = len(ring)
    area = ring[n - 1][1] * ring[0][0] - ring[n - 1][0] * ring[0][1]
    while i < n:
        i += 1
        area += ring[i - 1][1] * ring[i][0] - ring[i - 1][0] * ring[i][1]
    return area
