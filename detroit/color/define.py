def define(constructor, factory, prototype):
    constructor.prototype = factory.prototype = prototype
    prototype.constructor = constructor

def extend(parent, definition):
    prototype = type('Prototype', (parent,), {})
    for key, value in definition.items():
        setattr(prototype, key, value)
    return prototype
