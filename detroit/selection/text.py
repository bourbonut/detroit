def text_constant(value):
    def callback(node, data, i, group):
        node.text = value
    return callback

def text_function(value):
    def callback(node, data, i, group):
        node.text = value(data, i, group)
    return callable
