from pathlib import Path
import re

for file in Path().iterdir():
    if file.stem == "js2py":
        continue
    name = file.stem.split("-")[0]
    new_name = f"test_{name}.py"
    if match := re.findall(f"[A-Z]", new_name):
        c = match[0]
        new_name = new_name.replace(c, f"_{c.lower()}")
    file.rename(new_name)
