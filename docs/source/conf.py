# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'detroit'
copyright = '2024, bourbonut'
author = 'bourbonut'
release = "2.0.0"

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

html_theme_options = {
    "source_branch": "main",
    "source_directory": "docs/source/",
    "light_logo": "light-logo.svg",
    "dark_logo": "dark-logo.svg",
}

html_css_files = [
    'css/style.css',
]

html_title = f"Detroit v{release}"

napoleon_numpy_docstring = True
