# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class Plot_:
    """
    Class which mimick :code:`Plot`

    See `documentation <https://observablehq.com/plot/getting-started>`_.

    Examples
    --------

    >>> from detroit import Plot, js
    >>> Plot.dot(js("data"), {
    ...     "x": "Component 1",
    ...     "y": "Component 2",
    ...     "stroke": "digit",
    ...     "symbol": "digit",
    ... }).plot({
    ...     "symbol": {"legend": js("true")},
    ...     "color": {"scheme": "rainbow"},
    ... })
    Plot.dot(data, {'x': 'Component 1', 'y': 'Component 2', 'stroke': 'digit', 'symbol': 'digit'}).plot({'symbol': {'legend': true}, 'color': {'scheme': 'rainbow'}})

    Notes
    -----
    Do not use directly this class. Instead use :code:`detroit.Plot` or :code:`Plot = detroit.plot.Plot_()`.
    """
    def __init__(self, content: str = "Plot"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"
{% for name, args, format_args, docstring in methods %}
    def {{ name }}(self, {{ args }}):
        """
        {{ docstring }}
        """{% if format_args %}
        arguments = ", ".join(map(repr, filter(partial(is_not, None), {{ format_args }})))
        return Plot_(f"{self.content}.{{ name }}({arguments})")
{% else %}
        return Plot_(f"{self.content}.{{ name }}()")
{% endif %}
{% endfor %}
Plot = Plot_()
