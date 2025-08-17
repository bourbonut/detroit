from ..array import argpass

def matcher(match):
    if callable(match):
        return argpass(match)

    def match_func(d):
        return d == match

    return argpass(match_func)
