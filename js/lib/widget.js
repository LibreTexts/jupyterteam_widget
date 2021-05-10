var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');

// See jupyterteam_widget/widget.py for the kernel counterpart to this file.


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var HermiteWidgetModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : HermiteWidgetModel.model_name,
        _model_module : HermiteWidgetModel.model_module,
        _model_module_version : HermiteWidgetModel.model_module_version,
        _view_name : HermiteWidgetModel.view_name,
        _view_module : HermiteWidgetModel.view_module,
        _view_module_version : HermiteWidgetModel.view_module,
        value : 'Hello World!'
    })
});


// Custom View. Renders the widget model.
var HermiteWidgetView = widgets.DOMWidgetView.extend({
    // Defines how the widget gets rendered into the DOM
    render: function() {
        this.value_changed();

        // Observe changes in the value traitlet in Python, and define
        // a custom callback.
        this.model.on('change:value', this.value_changed, this);
    },

    value_changed: function() {
        this.el.textContent = this.model.get('value');
    }
});


module.exports = {
    HermiteWidgetModel: HermiteWidgetModel,
    HermiteWidgetView: HermiteWidgetView
};
