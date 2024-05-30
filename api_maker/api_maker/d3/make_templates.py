import re
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

SIGNATURE = re.compile(r"\((.*)\)")

def group_methods(sections):
    """
    Group methods per section
    """
    groups = []
    for methods in sections:
        group = {}
        for method in methods:
            insert(method, group)
        groups.append(group)
    return groups

def insert(method, group):
    """
    Insert the method in the group
    """
    name = method.name
    if "[" in name: # javascript iterators
        return
    if "d3." in name: # main methods
        group[name] = {"_primary": method.docstring}
    elif "new" in name: # special methods starting with "new d3.xxx"
        name = name.replace("new ", "new d3.")
        group[name] = {"_primary": method.docstring}
    elif "." in name: # submethods "prefix.suffix(...)"
        prefix, suffix = name.split(".")
        found = False
        for method_name in group:
            if prefix.lower() in method_name.lower():
                group[method_name][suffix] = method.docstring
                found = True
        if not found: # convert submethod as a main method
            name = f"d3.{prefix}"
            group[name] = {"_primary": [f"{prefix}()", f"\nSee more informations `here <{method.url}>`_."]}
            group[name][suffix] = method.docstring
    else: # if method has no bracket
        for method_name in group: # mix it with a main method
            if name.lower() in method_name.lower():
                docstring = group[method_name]["_primary"]
                docstring[0] = method.docstring[0]
                docstring.extend(method.docstring[1:])
                group[method_name]["_primary"] = docstring
                return

        # if return was not called 
        # try to mix it with a main method but with a new name
        name = f"d3.{name}"
        if name in group: # mix docstring
            docstring = group[name]["_primary"]
            docstring[0] = method.docstring[0]
            docstring.extend(method.docstring[1:])
            group[name]["_primary"] = docstring
        else:
            group[name] = {"_primary": method.docstring} # make a main method

def remove_blank(line: str):
    """
    Remove blank of a line
    """
    no_blank = line.replace(" ", "")
    if not no_blank:
        return no_blank
    return line

def remove_first_blank(docstring: list):
    """
    Remove first blank of a section
    """
    if not docstring[0] and len(docstring) > 1:
        docstring = docstring[1:]
        docstring[0] = docstring[0][8:]
        return docstring
    return docstring
    
def format_docstring(docstring: list):
    """
    Format the docstring to be used in templates
    """
    signature = docstring[0].replace("\u200b", "")
    docstring = "\n        ".join("\n".join(docstring[1:]).split("\n"))
    docstring = "\n".join(map(remove_blank, remove_first_blank(docstring.split("\n"))))
    match = SIGNATURE.findall(signature)
    if match:
        match = match[0] 
    if "[k]" in signature or not match:
        return "", "", docstring
    elif "..." in signature: # "..." is "*" in python
        args = match
        format_args = args.replace("...", "*")
        args = args.replace("...", "*")
        format_args = f"({format_args})" if "," in format_args else f"({format_args},)"
    elif "blur2" in signature: # special signature
        args = "matrix=None, rx=None, ry=None"
        format_args = "(matrix, rx, ry)"
    else:
        format_args = match.replace("lambda", "lambda_") # native python keyword
        if "3" in format_args: # special default argument
            args = format_args.replace(" = 3", "=3")
            format_args = format_args.replace(" = 3", "")
        else:
            args = ", ".join((f"{arg}=None" for arg in format_args.split(", "))) if format_args else ""
        if format_args: # add a comma if there is only one argument to make a tuple
            format_args = f"({format_args})" if "," in format_args else f"({format_args},)"
    return args, format_args, docstring

def make_templates(sections):
    """
    Make d3 API from sections using templates "templates/d3.py" and "templates/d3_subclass.py"
    """
    groups = group_methods(sections)

    # correction of locale and extract selection
    selection_groups = []
    locale = "d3.locale"
    selection = "d3.selection"
    for group in groups:
        contains_locale = locale in group.keys()
        if contains_locale and len(group[locale]) == 3:
            group["d3.format"]["_primary"].extend(group[locale]["format"][1:])
            group["d3.formatPrefix"]["_primary"].extend(group[locale]["formatPrefix"][1:])
            group.pop(locale)
        elif contains_locale and len(group[locale]) == 5:
            group["d3.timeFormat"]["_primary"].extend(group[locale]["format"][1:])
            group["d3.timeParse"]["_primary"].extend(group[locale]["parse"][1:])
            group["d3.utcFormat"]["_primary"].extend(group[locale]["utcFormat"][1:])
            group["d3.utcParse"]["_primary"].extend(group[locale]["utcParse"][1:])
            group.pop(locale)
        elif selection in group.keys():
            selection_groups.append(group.pop("d3.selection"))       


    # make selection as a unique class
    mix_selection = {}
    for selection_methods in selection_groups:
        for method_name, docstring in selection_methods.items():
            if method_name in mix_selection:
                mix_selection[method_name].extend(docstring[1:])
            else:
                mix_selection[method_name] = docstring

    # add selection methods in d3.select and d3.selectAll
    select = "d3.select"
    select_all = "d3.selectAll"
    _primary = mix_selection.pop("_primary")
    for group in groups:
        if select in group.keys() and select_all in group.keys():
            group[select].update(mix_selection)
            group[select_all].update(mix_selection)
    mix_selection["_primary"] = _primary

    # add selection class
    groups.append({"d3.selection": mix_selection})
    
    # seperate groups
    simple_methods = [] # simple methods with only _primary as method
    subclasses = [] # subclasses for d3.py template
    submethods = {} # submethods for d3_subclass.py template
    for i, group in enumerate(groups):
        for class_ in group:
            if len(group[class_]) == 1:
                docstring = format_docstring(group[class_]["_primary"])
                simple_methods.append((class_, *docstring))
            else:
                docstring = format_docstring(group[class_]["_primary"])
                subclasses.append((class_, *docstring))
                methods_ = []
                submethods[class_.replace("d3.", "").replace("new ", "")] = methods_
                for method in group[class_]:
                    if method != "_primary":
                        docstring = format_docstring(group[class_][method])
                        methods_.append((method, *docstring))

    # Make templates
    directory = Path("../detroit/d3")
    directory.mkdir(exist_ok=True)
    loader = FileSystemLoader([Path("api_maker/templates")])
    env = Environment(loader=loader, autoescape=select_autoescape())
    d3_template = env.get_template("d3.py")
    subclass_template = env.get_template("d3_subclass.py")
    for class_, methods in submethods.items():
        result = subclass_template.render(methods=methods, class_name=class_)
        with open(directory / f"{class_.replace('select', '_select')}.py", "w") as file:
            file.write(result)

    result = d3_template.render(methods=simple_methods, subclasses=subclasses)
    with open(directory / "__init__.py", "w") as file:
        file.write(result)
