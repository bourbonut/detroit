from copy import copy


def clone(node):
    clone = copy(node)
    parent = node.getparent()
    if parent is not None:
        parent.insert(0, clone)
    return [clone]
