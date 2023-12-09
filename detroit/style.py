from collections import namedtuple
from enum import Enum
from pathlib import Path

CENTER = {"display": "flex", "justify-content": "center"}

Style = namedtuple("Style", ["plot", "body"])

class Theme(Enum):
    JUPYTER_DARK = "jupyter_dark"
    JUPYTER_DARK_CENTER = "jupyter_dark_center"
    DARK = "dark"

def body(dictionary):
    caracteristics = "\n  ".join((f"{key}: {item};" for key, item in dictionary.items()))
    exlines = caracteristics.join(("{\n  ", "\n}"))
    return f"body{exlines}"

def style(theme):
    if theme == Theme.JUPYTER_DARK:
        plot_colors = {"backgroundColor": "#111111", "color": "white"}
        body_colors = {"background": "#111111", "color": "white"}
        return Style(plot_colors, body(body_colors))
    elif theme == Theme.JUPYTER_DARK_CENTER:
        plot_colors = {"backgroundColor": "#111111", "color": "white"}
        body_colors = {"background": "#111111", "color": "white"}
        return Style(plot_colors, body(body_colors | CENTER))
    elif theme == Theme.DARK:
        plot_colors = {"backgroundColor": "black", "color": "white"}
        body_colors = {"background": "black", "color": "white"}
        return Style(plot_colors, body(body_colors))
    else:
        raise ValueError(f"Theme {theme} not available.")
