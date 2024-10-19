from pathlib import Path
import re

PATH = Path(".")
PATTERN = re.compile(r"  assert ([a-z_]*).([a-z]*)")

for file in PATH.iterdir():
    if file.is_file() and "format_file" not in str(file):
        new_content = []
        content = file.read_text()
        lines = content.split("\n")
        block = False
        current_block = ""
        test_title = ""
        for line in lines:
            if "import" in line:
                if "datetime" in line:
                    new_content.append("from datetime import datetime")
                else:
                    new_content.append("import detroit as d3")
                continue
            elif "it(" in line:
                block = True
                continue
            if block:
                match = PATTERN.match(line)
                if match is None:
                    block = False
                    new_content.append("def test_unknown():")
                    new_content.append(line)
                    continue
                else:
                    test_title = match[1]
                    current_block = match[2]
                    block = False
                    new_content.append(f"def test_{test_title}_{current_block}():")
                    new_content.append(line)
            else:
                new_content.append(line)
        file.write_text("\n".join(new_content))
