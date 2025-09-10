<p align="center">
    <img style="border-radius:15px" src="https://raw.githubusercontent.com/bourbonut/detroit/main/docs/source/_static/logo.png"></img>
    <br />
    <a style="text-decoration: none;" href="https://pypi.org/project/detroit/">
        <img src="https://img.shields.io/pypi/v/detroit.svg?style=flat&logo=pypi" alt="PyPI Latest Release">
    </a>
    <a style="text-decoration: none;" href='https://detroit.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/detroit/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a style="text-decoration: none;" href="https://opensource.org/licenses/ISC">
        <img src="https://img.shields.io/badge/License-ISC-blue.svg" alt="Licence ISC">
    </a>
</p>

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
| array           | Yes      | Yes      |  Not all functions supported                                     |
| axis            | Yes      | Yes      |                                                                  |
| brush           | No       | -        |  TODO [`detroit-live`](https://github.com/bourbonut/detroit-live)|
| chord           | No       | -        |                                                                  |
| color           | Yes      | Yes      |                                                                  |
| contour         | Yes      | Yes      |                                                                  |
| delaunay        | No       | -        |                                                                  |
| dispatch        | No       | -        | TODO [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| drag            | No       | -        | TODO [`detroit-live`](https://github.com/bourbonut/detroit-live) |
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
| scale           | Yes      | Yes      | Mostly `test_linear`                                             |
| scale-chromatic | Yes      | Yes      |                                                                  |
| selection       | Yes      | Yes      |                                                                  |
| shape           | Yes      | Yes      |                                                                  |
| time            | Yes      | Yes      |                                                                  |
| time-format     | Yes      | Yes      |                                                                  |
| timer           | No       | -        | TODO [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| transition      | No       | -        | TODO [`detroit-live`](https://github.com/bourbonut/detroit-live) |
| zoom            | No       | -        | TODO [`detroit-live`](https://github.com/bourbonut/detroit-live) |
