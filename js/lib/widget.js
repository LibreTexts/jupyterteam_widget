var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var version = '0.1.0';

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
        _model_name : 'HermiteWidgetModel',
        _model_module : 'jupyterteam_widget',
        _model_module_version : version,
        _view_name : 'HermiteWidgetView',
        _view_module : 'jupyterteam_widget',
        _view_module_version : version,
    })
});

// Custom View. Renders the widget model.
var HermiteWidgetView = widgets.DOMWidgetView.extend({
    _onInputChanged: function() {
        console.log("initial backend value = ", this.model.get('value'));
        let tempval = this._valueInput.value;
        console.log("value from input box = ", tempval);
        this.model.set('value', tempval);
        console.log("value from backend = ", this.model.get('value'));
        this.model.save_changes();
        this.el.textContent = this.model.get('polystring');
    },

    // Defines how the widget gets rendered into the DOM
    render: function() {
        // input box
        this._valueInput = document.createElement('input');
        this._valueInput.type = "number";
        this.el.appendChild(this._valueInput);

        // Get Polynomial button
        this._valueSubmit = document.createElement('input');
        this._valueSubmit.type = "button";
        this._valueSubmit.value = "Get polynomial";
        this.el.appendChild(this._valueSubmit);

        // display the polynomial when button clicked
        this._valueSubmit.onclick = () => {
            this._onInputChanged();
        };
    }
});

module.exports = {
    HermiteWidgetModel: HermiteWidgetModel,
    HermiteWidgetView: HermiteWidgetView
};