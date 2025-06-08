from ..series import Series

def order_reverse(series: list[Series]) -> list[int]:
    return list(reversed(range(len(series))))
