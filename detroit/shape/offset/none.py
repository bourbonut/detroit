from ..series import Series

def offset_none(series: list[Series], order: list[int]):
    if len(series) == 0:
        return
    s1: Series = series[order[0]]
    m = len(s1)
    for i in range(1, len(series)):
        s0: Series = s1
        s1: Series = series[order[i]]
        for j in range(m):
            result = s0[j][0] if s0[j][1] is None else s0[j][1]
            s1[j][0] = result
            s1[j][1] += result
