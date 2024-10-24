from pathlib import Path

ROOT = Path()
FILE = Path("scale_chromatic.py")

lines = FILE.read_text().split("\n")
current_file = None
content = []
has_changed = False
for line in lines:
    if "# src/" in line:
        if file := current_file:
            file.write_text("\n".join(content))
        current_file = ROOT / "/".join(line.split("/")[1:])
        content = []
        continue
    content.append(line)

if (file := current_file) and content:
    file.write_text("\n".join(content))
