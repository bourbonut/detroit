def attr_function(name, value):
    def callback(node, data, i, group):
        node.set(name, str(value(data, i, group)))

    return callback


def attr_constant(name, value):
    def callback(node, data, i, group):
        node.set(name, str(value))

    return callback
