from inspect import signature


def text_constant(value):
    def callback(node, data, i, group):
        node.text = value

    return callback


def text_function(value):
    nargs = len(signature(value).parameters)

    def callback(node, data, i, group):
        args = [data, i, group][:nargs]
        node.text = value(*args)

    return callback
