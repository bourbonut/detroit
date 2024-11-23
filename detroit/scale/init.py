def init_range(obj, domain=None, range_vals=None):
    if domain is None and range_vals is None:
        return obj
    elif domain is None:
        return obj.range(range_vals)
    else:
        return obj.range(range_vals).domain(domain)

def init_interpolator(obj, domain=None, interpolator=None):
    if domain is None and interpolator is None:
        pass
    elif domain is not None:
        if callable(domain):
            obj.interpolator(domain)
        else:
            obj.range(domain)
    else:
        obj.domain(domain)
        if callable(interpolator):
            obj.interpolator(interpolator)
        else:
            obj.range(interpolator)
    return obj
