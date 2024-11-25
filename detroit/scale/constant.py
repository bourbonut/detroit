def constant(x):
    def f(*args):
        return x

    return f
