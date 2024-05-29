from functools import partial
from operator import is_not{% for name, args, format_args, docstring in subclasses %}
from {{ name.replace("d3.", "").replace("new ", "") }} import {{ name.replace("d3.", "").replace("new ", "") }}{% endfor %}

class d3:
    """
    Class used to mimick javascript syntax for :code:`d3`

    See `documentation <https://d3js.org/getting-started>`_.

    Examples
    --------

    >>> from detroit import d3, js
    >>> d3.axisBottom(js("x")).tickFormat(d3.format(".0f"))
    d3.axisBottom(x).tickFormat(d3.format('.0f'))
    """
    def __init__(self, content="d3"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
{% for name, args, format_args, docstring in methods %}
    @staticmethod
    def {{ name.replace("d3.", "").replace("new ", "") }}({{ args }}):
        """
        {{ docstring }}
        """{% if format_args %}
        arguments = ", ".join(map(str, filter(partial(is_not, None), {{ format_args }})))
        return d3(f"{{ name }}({arguments})")
{% else %}
        return d3("{{ name }}()")
{% endif %}{% endfor %}
{% for name, args, format_args, docstring in subclasses %}
    @staticmethod
    def {{ name.replace("d3.", "").replace("new ", "") }}({{ args }}):
        """
        {{ docstring }}
        """{% if format_args %}
        arguments = ", ".join(map(str, filter(partial(is_not, None), {{ format_args }})))
        return {{ name.replace("d3.", "").replace("new ", "") }}(f"{{ name }}({arguments})"){% else %}
        return {{ name.replace("d3.", "").replace("new ", "") }}("{{ name }}()"){% endif %}
{% endfor %}
