jupyterteam_widget
===============================

Widget for learning about Comm behavior

Development
------------

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)), these are only necessary on first install

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

You then need to refresh the JupyterLab page when your javascript changes. You may also use `yarn run watch` to continuously rebuild the widget as you change the Javascript.

The widget may be viewed by importing with `import jupyterteam_widget`. See the `example-notebook.ipynb` for an example.

Installation
------------

To install use pip:

    $ pip install jupyterteam_widget

Useful Documentation
------------

 - [TS Widget Tutorial](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Custom.html)
 - [JS Widget Tutorial](https://minrk-ipywidgets.readthedocs.io/en/latest/examples/Widget%20Custom.html) (possibly outdated)
 - [Widgets in HTML Pages](https://ipywidgets.readthedocs.io/en/latest/embedding.html)
