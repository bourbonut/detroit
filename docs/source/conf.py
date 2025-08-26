# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from datetime import datetime

import detroit

current_year = datetime.now().year
project = 'detroit'
copyright = f'2024-{current_year}, bourbonut'
author = 'bourbonut'
release = detroit.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.video",
]

templates_path = ['_templates']
exclude_patterns = []

root_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_favicon = '_static/favicon.ico'

html_css_files = ['style.css']

html_theme_options = {
    "source_branch": "main",
    "source_directory": "docs/source/",
    "light_logo": "light-logo.svg",
    "dark_logo": "dark-logo.svg",
}

# html_css_files = [
#     'css/style.css',
# ]

html_title = f"Detroit v{release}"

napoleon_numpy_docstring = True
