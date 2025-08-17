from ..array import argpass
from .enter import EnterNode


def bind_index(node_data, parent, group, enter, update, exit, data, _):
    for i in range(len(data)):
        node = group[i] if i < len(group) else None
        if node is not None:
            node_data[node] = data[i]
            update[i] = node
        else:
            enter[i] = EnterNode(parent, data[i])

    for i in range(len(data), len(group)):
        node = group[i] if i < len(group) else None
        if node is not None:
            exit[i] = node


def bind_key(node_data, parent, group, enter, update, exit, data, key):
    node_by_key_value = {}
    key_values = [None] * len(group)
    key = argpass(key)

    for i in range(len(group)):
        node = group[i]
        if node is not None:
            key_value = key(node_data.get(node), i, group)
            if key_value in node_by_key_value:
                exit[i] = node
            else:
                node_by_key_value[key_value] = node

    for i in range(len(data)):
        key_value = key(data[i], i, data)
        node = node_by_key_value.get(key_value)
        if node is not None:
            update[i] = node
            node_data[node] = data[i]
            del node_by_key_value[key_value]
        else:
            enter[i] = EnterNode(parent, data[i])

    for i in range(len(group)):
        node = group[i]
        if node is not None and node_by_key_value.get(key_values[i]) == node:
            exit[i] = node
