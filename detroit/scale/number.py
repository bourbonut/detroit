from datetime import datetime

def number(x):
    if isinstance(x, datetime):
        return x.timestamp()
    elif isinstance(x, str):
        return float(x)
    return x
