<h1 align="center">
    <img src="https://raw.githubusercontent.com/bourbonut/detroit/main/docs/source/_static/logo.png"></img>
</h1>

[![PyPI Latest Release](https://img.shields.io/pypi/v/detroit.svg?style=flat&logo=pypi)](https://pypi.org/project/detroit/)
[![Documentation Status](https://readthedocs.org/projects/detroit/badge/?version=latest)](https://detroit.readthedocs.io/en/latest/?badge=latest)
[![Licence ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)

`detroit` is Python implementation of [d3js](https://d3js.org/).

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

| Package Name    | Yes / No | Tests OK | Notes                                                            |
|-----------------|----------|----------|------------------------------------------------------------------|
| array           | Yes      | Yes      | Not all functions supported                                      |
| axis            | Yes      | Yes      |                                                                  |
| brush           | -        | -        | TODO [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| chord           | No       | -        |                                                                  |
| color           | Yes      | Yes      |                                                                  |
| contour         | Yes      | Yes      |                                                                  |
| delaunay        | No       | -        |                                                                  |
| dispatch        | -        | -        | See  [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| drag            | -        | -        | See  [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| dsv             | -        | -        | use `import pandas / polars`                                     |
| ease            | No       | -        |                                                                  |
| fetch           | -        | -        | use `import requests`                                            |
| force           | No       | -        |                                                                  |
| format          | Yes      | Yes      |                                                                  |
| geo             | Yes      | Yes      |                                                                  |
| hierarchy       | No       | -        |                                                                  |
| interpolate     | Yes      | Yes      | interpolate CSS not supported                                    |
| path            | Yes      | Yes      |                                                                  |
| polygon         | No       | -        |                                                                  |
| quadtree        | No       | -        |                                                                  |
| random          | -        | -        | Use `import random`                                              |
| scale           | Yes      | Yes      |                                                                  |
| scale-chromatic | Yes      | Yes      |                                                                  |
| selection       | Yes      | Yes      |                                                                  |
| shape           | Yes      | Yes      |                                                                  |
| time            | Yes      | Yes      |                                                                  |
| time-format     | Yes      | Yes      |                                                                  |
| timer           | -        | -        | See  [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| transition      | -        | -        | TODO [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| zoom            | -        | -        | See  [`detroit-live`](https://github.com/bourbonut/detroit-live) |
