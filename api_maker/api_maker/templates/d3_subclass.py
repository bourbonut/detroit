from functools import partial
from operator import is_not

class {{ class_name.replace("bin", "_bin") }}:
    def __init__(self, content="{{class_name}}"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
{% for name, args, format_args, docstring in methods %}{% if format_args %}
    def {{ name.replace("from", "from_") }}(self, {{ args }}):{% else %}
    def {{ name.replace("raise", "raise_") }}(self):{% endif %}
        """
        {{ docstring }}
        """{% if format_args %}
        arguments = ", ".join(map(str, filter(partial(is_not, None), {{ format_args }})))
        return {{class_name}}(content=f"{self.content}.{{ name }}({arguments})")
{% else %}
        return {{class_name}}(content=f"{self.content}.{{ name }}()")
{% endif %}
{% endfor %}
