from inspect import signature


def style_function(name, value):
    nargs = len(signature(value).parameters)

    def callback(node, data, i, group):
        args = [data, i, group][:nargs]
        current_value = node.get("style", "")
        new_value = value(*args)
        node.set("style", f"{current_value}{name}:{new_value};")

    return callback


def style_constant(name, value):
    def callback(node, data, i, group):
        current_value = node.get("style", "")
        node.set("style", f"{current_value}{name}:{value};")

    return callback


def style_value(style, name):
    if style.endswith(";"):
        style = style[:-1]
    attrs = {
        property: value
        for property, value in (desc.split(":") for desc in style.split(";"))
    }
    return attrs.get(name)
