from functools import partial
from operator import is_not

class Plot:
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
    """
    def __init__(self, content: str = "Plot"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
{% for name, args, format_args, docstring in methods %}
    @staticmethod
    def {{ name }}({{ args }}):
        """
        {{ docstring }}
        """{% if format_args %}
        arguments = ", ".join(map(str, filter(partial(is_not, None), ({{ format_args }}))))
        return Plot(f"Plot.{{ name }}({arguments})")
{% else %}
        return Plot(f"Plot.{{ name }}()")
{% endif %}
{% endfor %}