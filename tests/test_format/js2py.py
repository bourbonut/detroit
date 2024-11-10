from pathlib import Path
import re

ASSERT_PATTERN = re.compile(r'([ ]*)assert.[a-zA-Z]*\(([#a-zA-Z0-9\(\)\-\+.:" ;\/]*), ([#a-zA-Z0-9\(\-\+:." ,\);\/]*)\);')
ASSERT_PATTERN2 = re.compile(r'([ ]*)assert.[a-zA-Z]*\(([a-zA-Z0-9\(\)\-." ]*), \[')

def format_line(line):
    line = ASSERT_PATTERN.sub(r"\1assert \2 == \3", line)
    line = ASSERT_PATTERN2.sub(r"\1assert \2 == [", line)
    line = line.replace("const ", "").replace(";", "").replace(" " * 2, " " * 4)
    line = line.replace("NaN", "math.nan").replace("Infinity", "math.inf").replace("undefined", "None").replace("null", "None")
    return line

def format_file(file: Path, name: str):
    new_content = []
    content = file.read_text()
    lines = content.split("\n")
    block = False
    import_done = False
    test_number = 1
    for line in lines:
        if "import" in line:
            if import_done:
                continue
            new_content.append("import detroit as d3")
            import_done = True
            continue
        elif "it(" in line:
            block = True
            continue
        if block:
            block = False
            new_content.append(f"def test_{name}_{test_number}():")
            test_number += 1
            new_content.append(format_line(line))
            continue
        elif line == "});":
            continue
        else:
            new_content.append(format_line(line))
    file.write_text("\n".join(new_content))

def rename_file_to_py(file):
    name = "_".join(file.stem.split("-")[:-1])
    new_name = f"test_{name}.py"
    if match := re.findall(r"[A-Z]", new_name):
        c = match[0]
        new_name = new_name.replace(c, f"_{c.lower()}").replace("-", "_")
    return new_name, name

for file in Path().iterdir():
    if file.stem == "js2py":
        continue

    new_name, name = rename_file_to_py(file)
    format_file(file, name)
    file.rename(new_name)
