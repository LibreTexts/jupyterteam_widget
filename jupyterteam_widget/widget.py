from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Int, validate, TraitError

from ._frontend import module_name, module_version

# See js/lib/widget.js for the frontend counterpart to this file.

@register
class HermiteWidget(DOMWidget, ValueWidget):
    # Name of the widget model class in front-end
    _model_name = Unicode('HermiteWidgetModel').tag(sync=True)
    # Name of the front-end module containing widget model
    _model_module = Unicode(module_name).tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(module_version).tag(sync=True)

    # Name of the widget view class in front-end
    _view_name = Unicode('HermiteWidgetView').tag(sync=True)
    # Name of the front-end module containing widget view
    _view_module = Unicode(module_name).tag(sync=True)
    # Version of the front-end module containing widget view
    _view_module_version = Unicode(module_version).tag(sync=True)

    # Widget specific property.
    # Widget properties are defined as traitlets. Any property tagged with `sync=True`
    # is automatically synced to the frontend *any* time it changes in Python.
    # It is synced back to Python from the frontend *any* time the model is touched.
    value = Int(1).tag(sync=True)
