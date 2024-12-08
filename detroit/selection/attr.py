from inspect import signature


def attr_function(name, value):
    nargs = len(signature(value).parameters)

    def callback(node, data, i, group):
        args = [data, i, group][:nargs]
        node.set(name, str(value(*args)))

    return callback


def attr_constant(name, value):
    def callback(node, data, i, group):
        node.set(name, str(value))

    return callback
