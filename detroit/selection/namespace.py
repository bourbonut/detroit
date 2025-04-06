NAMESPACES = {
    "svg": {None: "http://www.w3.org/2000/svg"},
    # 'xhtml': xhtml,
    # 'xlink': "http://www.w3.org/1999/xlink",
    # 'xml': "http://www.w3.org/XML/1998/namespace",
    # 'xmlns': "http://www.w3.org/2000/xmlns/"
}


def namespace(name: str):
    prefix = name
    i = prefix.find(":")
    if i >= 0 and (prefix := name[:i]) != "xmlns":
        name = name[i + 1 :]
    return (
        {"space": NAMESPACES[prefix], "local": name} if prefix in NAMESPACES else name
    )
