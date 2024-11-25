from datetime import datetime


def number(x):
    # if isinstance(x, datetime):
    #     return x.timestamp()
    if isinstance(x, str):
        return float(x)
    return x
