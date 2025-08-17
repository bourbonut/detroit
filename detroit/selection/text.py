from ..array import argpass


def text_constant(value):
    def callback(node, data, i, group):
        node.text = value

    return callback


def text_function(value):
    value = argpass(value)

    def callback(node, data, i, group):
        node.text = value(data, i, group)

    return callback
