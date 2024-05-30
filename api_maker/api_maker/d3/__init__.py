from .from_api import scrap_methods
from .make_templates import make_templates
import asyncio
import pickle
from pathlib import Path

def fill_d3_template(cache_file_path="d3_sections.pkl", cache=True):
    if not cache:
        make_templates(asyncio.run(scrap_methods()))
        return

    cache_file = Path(cache_file_path)
    if cache_file.exists():
        with open(cache_file, "rb") as file:
            sections = pickle.load(file)
    else:
        sections = asyncio.run(scrap_methods())
        with open(cache_file, "wb") as file:
            pickle.dump(sections, file)
    make_templates(sections)
    return
