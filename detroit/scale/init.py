def init_range(obj, domain=None, range_vals=None):
    if domain is None and range_vals is None:
        return obj
    elif domain is None:
        return obj.range(domain)
    else:
        return obj.range(range_vals).domain(domain)

def init_interpolator(domain=None, interpolator=None):
    if domain is None and interpolator is None:
        pass
    elif domain is not None:
        if callable(domain):
            this.interpolator(domain)
        else:
            this.range(domain)
    else:
        this.domain(domain)
        if callable(interpolator):
            this.interpolator(interpolator)
        else:
            this.range(interpolator)
    return this
