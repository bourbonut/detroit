def init_range(obj, domain=None, range_vals=None):
    if domain is None and range_vals is None:
        return obj
    elif domain is None:
        return obj.set_range(range_vals)
    else:
        return obj.set_range(range_vals).set_domain(domain)

def init_interpolator(obj, domain=None, interpolator=None):
    if domain is None and interpolator is None:
        return obj
    elif domain is not None:
        obj.set_domain(domain)
        if callable(domain):
            obj.set_interpolator(domain)
        else:
            obj.set_range(domain)
    else:
        if callable(interpolator):
            obj.set_interpolator(interpolator)
        else:
            obj.set_range(interpolator)
    return obj
