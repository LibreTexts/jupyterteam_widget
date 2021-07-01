var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var Plotly = require('plotly.js-dist-min');

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
        this._valueInput = document.createElement('input');
        this._valueInput.type = "range";
        this._valueInput.min = "0";
        this._valueInput.max = "10";
        this._valueInput.value = "5";
        this.el.appendChild(this._valueInput);
        
        this.model.set('value', parseInt(this._valueInput.value));
        this.model.save_changes();

        this._output = document.createElement('p');
        this._output.innerHTML = "";
        this.el.appendChild(this._output);

        this._HERMITE_PLOT = document.createElement('div');
        this._HERMITE_PLOT.id = "HERMITE_PLOT";
        this.el.appendChild(this._HERMITE_PLOT);

        // JS change detection
        this._valueInput.oninput = this._on_HTML_change.bind(this);

        // // Observe changes in the value traitlet in Python, and define
        // // a custom callback.
        // this.model.on('change:polystring', this._value_changed, this);

        this.model.on('change:plot_data', this._replot_HERMITE_PLOT, this);
    },

    _on_HTML_change: function() {
      // this._output.innerHTML = this.model.get('polystring');
      this._output.innerHTML = "Value: " + this._valueInput.value;
      let inputValue = parseInt(this._valueInput.value);
      if(isNaN(inputValue) || inputValue < 0 || inputValue > 10) {
          this._output.innerHTML = "Invalid input! Please make sure you are inputting an integer between 0 and 10";
      } else {
      this.model.set('value', inputValue);
      this.model.save_changes();
      }
    },

    _value_changed: function() {
        this._output.innerHTML = this.model.get('polystring');
    },

    _replot_HERMITE_PLOT: function() {
        let data_title = "N = " + this.model.get("value");
        let tempval = (this.model.get("value") - 1);
        if (tempval < 0) tempval++;

        let data = [{
            "x": this.model.get('plot_data')[0],
            "y": this.model.get('plot_data')[1],
        }];

        let layout = {
            title: data_title,
            xaxis: {
              title: {
                text: 'x',
              },
            },
            yaxis: {
              title: {
                text: 'H(x)',
              }
            }
        }

        Plotly.newPlot("HERMITE_PLOT", data, layout, {scrollZoom: false, displaylogo: false});

    },
});

module.exports = {
    HermiteWidgetModel: HermiteWidgetModel,
    HermiteWidgetView: HermiteWidgetView
};
