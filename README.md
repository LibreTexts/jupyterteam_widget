jupyterteam_widget
===============================

Widget for learning about Comm behavior

Development
------------

Run the following to locally install the widget;

    $ git clone https://github.com/LibreTexts/jupyterteam_widget.git
    $ cd jupyterteam_widget
    $ pip install -e .

To enable development mode, run;

    $ jupyter labextension develop --overwrite jupyterteam_widget

To build the Javascript, run;

    $ cd js
    $ yarn run build

You may also use `yarn run watch` to continuously rebuild the widget as you change the Javascript.

The widget may be viewed by importing with `import jupyterteam_widget`. See the `example-notebook.ipynb` for an example.

Default CookieCutter Installation
------------

This section was written by default upon creation of the repository by the cookiecutter template. Here for reference, but use the information above to install for development.

To install use pip:

    $ pip install jupyterteam_widget

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/LibreTexts/jupyterteam_widget.git
    $ cd jupyterteam_widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix jupyterteam_widget
    $ jupyter nbextension enable --py --sys-prefix jupyterteam_widget

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite jupyterteam_widget

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.

# Useful Documentation

 - [Widget Tutorial](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Custom.html)
 - [Widgets in HTML Pages](https://ipywidgets.readthedocs.io/en/latest/embedding.html)
