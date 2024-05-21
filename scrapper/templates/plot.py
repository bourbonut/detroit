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
        """
        return Plot(f"Plot.{{ name }}({{ format_args }})")
{% endfor %}
