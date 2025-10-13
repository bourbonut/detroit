def constant(x):
    def f(*args):
        return x

    return f


def constant_zero(*args):
    return 0
