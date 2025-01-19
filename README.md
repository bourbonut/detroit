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

`detroit` is Python implentation of [d3js](https://d3js.org/).

- [Documentation](https://detroit.readthedocs.io/en/latest/)
- [Examples](https://github.com/bourbonut/detroit/tree/main/examples)

<p align="center">
    <img style="width: 70%;" src="https://raw.githubusercontent.com/bourbonut/detroit/main/docs/source/figures/hertz_russel.png"></img>
    <br />
    <a href="https://github.com/bourbonut/detroit/blob/main/examples/hertz_russel.py">Source code</a>
</p>

# Installation

```sh
pip install detroit
```

# Coverage

| Package Name    | Yes / No | Tests OK | Notes                         |
|-----------------|----------|----------|-------------------------------|
| array           | Yes      | Yes      |  Not all functions supported  |
| axis            | Yes      | Yes      |                               |
| brush           | No       | -        |                               |
| chord           | No       | -        |                               |
| color           | Yes      | Yes      |                               |
| contour         | No       | -        |                               |
| delaunay        | No       | -        |                               |
| dispatch        | No       | -        |                               |
| drag            | No       | -        |                               |
| dsv             | -        | -        | use `import pandas / polars`  |
| ease            | No       | -        |                               |
| fetch           | -        | -        | use `import requests`         |
| force           | No       | -        |                               |
| format          | Yes      | Yes      |                               |
| geo             | No       | -        |                               |
| hierarchy       | No       | -        |                               |
| interpolate     | Yes      | Yes      | interpolate CSS not supported |
| path            | Yes      | Yes      |                               |
| polygone        | No       | -        |                               |
| quadtree        | No       | -        |                               |
| random          | -        | -        | Use `import random`           |
| scale           | Yes      | Yes      | Mostly `test_linear`          |
| scale-chromatic | Yes      | Yes      | See all schemes in `examples` |
| selection       | Yes      | No       | TODO: tests                   |
| shape           | Yes      | Yes      | Missing some of shapes        |
| time            | Yes      | Yes      |                               |
| time-format     | Yes      | Yes      |                               |
| timer           | No       | -        |                               |
| transition      | No       | -        |                               |
| zoom            | No       | -        |                               |
