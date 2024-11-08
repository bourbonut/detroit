def style_value(style, name):
    if style.endswith(";"):
        style = style[:-1]
    attrs = {property: value for property, value in (desc.split(":") for desc in style.split(";"))}
    return attrs.get(name)

