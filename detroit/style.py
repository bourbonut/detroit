import copy
from collections import namedtuple
from enum import Enum
from typing import Union, Optional
from pathlib import Path

CENTER = {"body": {"display": "flex", "justify-content": "center"}}
GRID = lambda ncol: {
    '.container': {'display': 'grid', 'grid-template-columns': ' '.join(['auto'] * ncol)},
    '.plot': {'display': 'flex', 'justify-content': 'center'},
    'h2': {'text-align': 'center'}
}

class Theme(Enum):
    JUPYTER_DARK = "jupyter_dark"
    JUPYTER_DARK_CENTER = "jupyter_dark_center"
    DARK = "dark"

class CSS:
    """
    Class which handles style from :

    * file input
    * string input
    * dictionary

    It can merge style together.

    Parameters
    ----------
    css : Optional[Union[str, dict]]
        CSS style stored into dictionary

    Examples
    --------

    From dictionary:

    >>> style_dict = {"body": {"background": "black"}}
    >>> print(CSS(style_dict))
    body {
      background: black;
    }

    From string :

    >>> style_str = \"\"\"body {
    ...     background: black;
    ... }
    ... \"\"\"
    >>> print(CSS(style_str))
    body {
        background: black;
    }

    From a file:

    >>> style = CSS("style.css")
    >>> print(style)
    body {
        background: black;
    }
    """
    def __init__(self, css: Optional[Union[str, dict]]=None):
        if css is None:
            self.css = {}
        elif isinstance(css, dict):
            self.css = css
        elif isinstance(css, str):
            css_path = Path(css)
            if css_path.exists():
                self.set_from_string(css_path.read_text())
            else:
                self.set_from_string(css)

    def set_from_string(self, string):
        subparts = [part.split("{") for part in string.split("}")]
        classes = {
            class_: [attr.split(":") for attr in attrs.split(";")]
            for class_, attrs in filter(lambda x: len(x) == 2, subparts)
        }
        self.css = {
            self.clean(class_): {
                self.clean(key): self.clean(item)
                for key, item in filter(lambda x: len(x) == 2, attrs)
            }
            for class_, attrs in classes.items()
        }

    def clean(self, string):
        return string.replace("\n ", "").replace("\n\n", "").removeprefix(" ").removesuffix(" ")

    def format_attr(self, attributs):
        return (
            "\n  ".join((f"{key}: {item};" for key, item in attributs.items()))
                  .join(("{\n  ", "\n}"))
        )

    def __str__(self):
        classes = {class_: self.format_attr(attributs) for class_, attributs in self.css.items()}
        return "\n\n".join((f"{class_} {item}" for class_, item in classes.items()))

    def update(self, css: dict):
        """
        Update its style css

        Parameters
        ----------
        css : dict
           style used for update 

        Examples
        --------

        >>> style = CSS("style.css")
        >>> print(style)
        body {
            background: black;
        }
        >>> style.update({"body": {"background": "white", "color": "blue"}})
        >>> print(style)
        body {
          background: white;
          color: blue;
        }
        """
        for common_key in self.css.keys() & css.keys():
            self.css[common_key].update(css[common_key])
        for new_key in css.keys() - self.css.keys():
            self.css[new_key] = css[new_key]

    def __or__(self, css):
        copy_ = CSS(copy.copy(self.css))
        copy_.update(css)
        return copy_

def style(theme):
    """
    Select a theme from Theme enum
    """
    Style = namedtuple("Style", ["plot", "body"])
    if theme == Theme.JUPYTER_DARK:
        plot_colors = {"backgroundColor": "#111111", "color": "white"}
        body_colors = {"body": {"background": "#111111", "color": "white"}}
        return Style(plot_colors, str(CSS(body_colors)))
    elif theme == Theme.JUPYTER_DARK_CENTER:
        plot_colors = {"backgroundColor": "#111111", "color": "white"}
        body_colors = {"body": {"background": "#111111", "color": "white"}}
        return Style(plot_colors, str(CSS(body_colors) | CENTER))
    elif theme == Theme.DARK:
        plot_colors = {"backgroundColor": "black", "color": "white"}
        body_colors = {"body": {"background": "black", "color": "white"}}
        return Style(plot_colors, str(CSS(body_colors)))
    else:
        raise ValueError(f"Theme {theme} not available.")
