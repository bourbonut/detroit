import copy
from collections import namedtuple
from enum import Enum
from typing import Union, Optional
from pathlib import Path

GRID = lambda ncol: {
    '.container': {'display': 'grid', 'grid-template-columns': ' '.join(['auto'] * ncol)},
    '.plot': {'display': 'flex', 'justify-content': 'center'},
    'h2': {'text-align': 'center'}
}

class Theme(Enum):
    """
    Enum class for available themes

    Attributes
    ----------
    JUPYTER_DARK : dict
        Dark Theme for Jupyter Notebook

    JUPYTER_DARK_CENTER : dict
        Dark Theme for Jupyter Notebook where visualization is centered

    DARK : dict
        Dark Theme (black and white)

    DARK_CENTER : dict
        Dark Theme (black and white) where visualization is centered

    CENTER : dict
        Visualization is centered

    Examples
    --------
    
    >>> from detroit import Theme
    >>> Theme.JUPYTER_DARK_CENTER.plot
    {'backgroundColor': '#111111', 'color': 'white'}
    >>> Theme.DARK.style
    {'body': {'background': 'black', 'color': 'white'}}
    """
    JUPYTER_DARK = {
        "plot": {"backgroundColor": "#111111", "color": "white"},
        "style": {"body": {"background": "#111111", "color": "white"}},
    }
    JUPYTER_DARK_CENTER = {
        "plot": {"backgroundColor": "#111111", "color": "white"},
        "style": {"body": {"background": "#111111", "color": "white", "display": "flex", "justify-content": "center"}},
    }
    DARK = {
        "plot": {"backgroundColor": "black", "color": "white"},
        "style": {"body": {"background": "black", "color": "white"}},
    }
    DARK_CENTER = {
        "plot": {"backgroundColor": "black", "color": "white"},
        "style": {"body": {"background": "black", "color": "white", "display": "flex", "justify-content": "center"}},
    }
    CENTER = {
        "plot": {},
        "style": {"body": {"display": "flex", "justify-content": "center"}},
    }

    @property
    def plot(self):
        return self.value["plot"]

    @property
    def style(self):
        return self.value["style"]


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

    >>> from detroit import CSS
    >>> style_dict = {"body": {"background": "black"}}
    >>> print(CSS(style_dict))
    body {
      background: black;
    }

    From string :

    >>> from detroit import CSS
    >>> style_str = \"\"\"body {
    ...     background: black;
    ... }
    ... \"\"\"
    >>> print(CSS(style_str))
    body {
        background: black;
    }

    From a file:

    >>> from detroit import CSS
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

        >>> from detroit import CSS
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
