# API Maker

This module scraps API of [d3js](https://d3js.org/api) and [Observable Plot](https://observablehq.com/plot/api) and injects it directly in `detroit` code.

```
$ python -m api_maker
usage: api_maker [-h] [--nocache] [--plot_file FILE] [--d3_file FILE] {all,d3,plot} ...

options:
  -h, --help        show this help message and exit
  --nocache         Disable cache
  --plot_file FILE  Plot pickle cache file
  --d3_file FILE    d3 pickle cache file

commands:
  {all,d3,plot}
    all             Make Plot API and d3 API
    d3              Make d3 API
    plot            Make Plot API
```
