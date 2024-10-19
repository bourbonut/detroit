def init_range(obj, domain=None, range_vals=None):
    if domain is None and range_vals is None:
        return
    elif domain is None:
        return obj.range(domain)
    else:
        return obj.range(range_vals).domain(domain)

