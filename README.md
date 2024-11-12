<p align="center">
    <img style="border-radius:15px" src="https://raw.githubusercontent.com/bourbonut/detroit/main/docs/source/_static/logo.png"></img>
    <br />
    <a href="https://pypi.org/project/detroit/">
        <img src="https://img.shields.io/pypi/v/detroit.svg?style=flat&logo=pypi" alt="PyPI Latest Release">
    </a>
    <a href='https://detroit.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/detroit/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://img.shields.io/badge/license-MIT-red.svg?style=flat">
        <img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" alt="BSD-3-Clause">
    </a>
</p>

detroit is Python implentation of [d3js](https://d3js.org/).

- [Documentation](https://detroit.readthedocs.io/en/latest/)

# Installation

```sh
pip install detroit
```

# Coverage

| Package Name                                           | Yes / No                                   | Tests OK | Notes                         |
|--------------------------------------------------------|--------------------------------------------|----------|-------------------------------|
| <span style="color:lightgreen;">array</span>           | <span style="color:lightgreen;">Yes</span> | Yes      | Some tests must be updated    |
| <span style="color:lightgreen;">axis</span>            | <span style="color:lightgreen;">Yes</span> | No       | TODO: tests                   |
| brush                                                  | No                                         | -        |                               |
| chord                                                  | No                                         | -        |                               |
| <span style="color:lightgreen;">color</span>           | <span style="color:lightgreen;">Yes</span> | Yes      |                               |
| contour                                                | No                                         | -        |                               |
| delaunay                                               | No                                         | -        |                               |
| dispatch                                               | No                                         | -        |                               |
| drag                                                   | No                                         | -        |                               |
| <del>dsv</del>                                         | No                                         | -        | use `import pandas / polars`  |
| ease                                                   | No                                         | -        |                               |
| <del>fetch</del>                                       | No                                         | -        | use `import requests`         |
| force                                                  | No                                         | -        |                               |
| <span style="color:lightgreen;">format</span>          | <span style="color:lightgreen;">Yes</span> | Yes      | Only `d3.format`              |
| geo                                                    | No                                         | -        |                               |
| hierarchy                                              | No                                         | -        |                               |
| <span style="color:lightgreen;">interpolate</span>     | <span style="color:lightgreen;">Yes</span> | Yes      | interpolate CSS not supported |
| <span style="color:lightgreen;">path</span>            | <span style="color:lightgreen;">Yes</span> | Yes      |                               |
| polygone                                               | No                                         | -        |                               |
| quadtree                                               | No                                         | -        |                               |
| <del>random</del>                                      | No                                         | -        | Use `import random`           |
| <span style="color:lightgreen;">scale</span>           | <span style="color:lightgreen;">Yes</span> | Yes      | Mostly `test_linear`          |
| <span style="color:lightgreen;">scale-chromatic</span> | <span style="color:lightgreen;">Yes</span> | No       | TODO: tests                   |
| <span style="color:lightgreen;">selection</span>       | <span style="color:lightgreen;">Yes</span> | No       | TODO: tests                   |
| <span style="color:lightgreen;">shape</span>           | <span style="color:lightgreen;">Yes</span> | Yes      | Missing most of shapes        |
| <span style="color:lightgreen;">time</span>            | <span style="color:lightgreen;">Yes</span> | Yes      | TODO: pass tests              |
| <span style="color:lightgreen;">time-format</span>     | <span style="color:lightgreen;">Yes</span> | Yes      |                               |
| timer                                                  | No                                         | -        |                               |
| transition                                             | No                                         | -        |                               |
| zoom                                                   | No                                         | -        |                               |
