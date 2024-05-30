import argparse
import sys
import logging

from .d3 import fill_d3_template
from .plot import fill_plot_template

logging.basicConfig(format="%(levelname)s - %(message)s (%(filename)s:%(lineno)d)", level=logging.INFO)
parser = argparse.ArgumentParser("api_maker")

parser.add_argument("--nocache", action="store_false", help="Disable cache")
parser.add_argument("--plot_file", metavar="FILE", default="plot_methods.pkl", help="Plot pickle cache file")
parser.add_argument("--d3_file", metavar="FILE", default="d3_sections.pkl", help="d3 pickle cache file")
commands = parser.add_subparsers(title="commands", dest="command")

commands.add_parser("all", help="Make Plot API and d3 API")
d3_parse = commands.add_parser("d3", help="Make d3 API")
plot_parse = commands.add_parser("plot", help="Make Plot API")

args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

if args.command == "all":
    fill_d3_template(args.d3_file, args.nocache)
    fill_plot_template(args.plot_file, args.nocache)
elif args.command == "d3":
    fill_d3_template(args.d3_file, args.nocache)
elif args.command == "plot":
    fill_plot_template(args.plot_file, args.nocache)
