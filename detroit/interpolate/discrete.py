def discrete(range_):
    n = len(range_)
    return lambda t: range_[max(0, min(n - 1, int(t * n)))]
