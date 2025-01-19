from inspect import signature

def matcher(match):
    if callable(match):
        nargs = len(signature(match).parameters)
        return match, nargs
    def match_func(d):
        return d == match
    return match_func, 1
