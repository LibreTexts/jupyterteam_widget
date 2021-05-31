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
    // Defines how the widget gets rendered into the DOM
    render: function() {
        this._valueSubmit = document.createElement('input');
        this._valueSubmit.type = "button";
        this._valueSubmit.value = "submit";
        this.el.appendChild(this._valueSubmit);

        this._valueInput = document.createElement('input');
        this._valueInput.type = "number";
        this.el.appendChild(this._valueInput);

        this._output = document.createElement('p');
        this._output.innerHTML = "";
        this.el.appendChild(this._output);

        this._valueSubmit.onclick = () => {
            let inputValue = parseInt(this._valueInput.value);
            if(!inputValue || inputValue < 0 || inputValue > 10) {
                this._output.innerHTML = "Invalid input! Please make sure you are inputting an integer between 0 and 10";
            } else {
            this.model.set('value', inputValue);
            this.model.save_changes();
            }
        };

        // // Observe changes in the value traitlet in Python, and define
        // // a custom callback.
        this.model.on('change:polystring', this._value_changed, this);
    },

    _value_changed: function() {
        this._output.innerHTML = this.model.get('polystring');
    },
});

module.exports = {
    HermiteWidgetModel: HermiteWidgetModel,
    HermiteWidgetView: HermiteWidgetView
};
