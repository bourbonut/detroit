from functools import partial
from operator import is_not

class Plot:
    def __init__(self, content="Plot"):
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
