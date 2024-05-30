from .from_api import scrap_methods
from .make_template import make_template

import asyncio
import pickle
from pathlib import Path

def fill_plot_template(cache_file_path="plot_methods.pkl", cache=True):
    if not cache:
        make_template(asyncio.run(scrap_methods()))
        return

    cache_file = Path(cache_file_path)
    if cache_file.exists():
        with open(cache_file, "rb") as file:
            methods = pickle.load(file)
    else:
        methods = asyncio.run(scrap_methods())
        with open(cache_file, "wb") as file:
            pickle.dump(methods, file)
    make_template(methods)
    return
