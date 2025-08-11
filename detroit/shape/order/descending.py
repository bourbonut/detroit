from .ascending import order_ascending
from ..series import Series

def order_descending(series: list[Series]) -> list[int]:
    return order_ascending(series)[::-1]
