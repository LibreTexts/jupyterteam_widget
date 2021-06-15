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
        this._valueSubmit = document.createElement('input');
        this._valueSubmit.type = "button";
        this._valueSubmit.value = "submit";
        this.el.appendChild(this._valueSubmit);

        this._valueInput = document.createElement('input');
        this._valueInput.type = "number";
        this._valueInput.autocomplete = "off";
        this.el.appendChild(this._valueInput);

        this._output = document.createElement('p');
        this._output.innerHTML = "";
        this.el.appendChild(this._output);

        this._first_four_plot = document.createElement('div');
        this._first_four_plot.id = "first_four_plot";
        this.el.appendChild(this._first_four_plot);

        this._PSI_NDMN = document.createElement('div');
        this._PSI_NDMN.id = "PSI_NDMN";
        this.el.appendChild(this._PSI_NDMN);

        this._PSI_NDMN_2 = document.createElement('div');
        this._PSI_NDMN_2.id = "PSI_NDMN_2";
        this.el.appendChild(this._PSI_NDMN_2);

        this._valueSubmit.onclick = () => {
            let inputValue = parseInt(this._valueInput.value);
            if(!inputValue || inputValue <= 0 || inputValue > 10) {
                this._output.innerHTML = "Invalid input! Please make sure you are inputting an integer between 0 and 10";
            } else {
            this.model.set('value', inputValue);
            this.model.save_changes();
            }
        };

        // // Observe changes in the value traitlet in Python, and define
        // // a custom callback.
        this.model.on('change:polystring', this._value_changed, this);

        this.model.on('change:psi_ndmn', this._replot_PSI_NDMN, this);

        this.model.on('change:first_four', this._replot_first_four, this);
    },

    _value_changed: function() {
        this._output.innerHTML = this.model.get('polystring');
    },

    _replot_first_four: function() {
        let data = [{
            "x": this.model.get('first_four')[0],
            "y": this.model.get('first_four')[1],
            "name": "n = 1"
        },{
            "x": this.model.get('first_four')[0],
            "y": this.model.get('first_four')[2],
            "name": "n = 2"
        },{
            "x": this.model.get('first_four')[0],
            "y": this.model.get('first_four')[3],
            "name": "n = 3"
        },{
            "x": this.model.get('first_four')[0],
            "y": this.model.get('first_four')[4],
            "name": "n = 4"
        }];

        let layout = {
            title:"Hermite Polynomials n = 1 to 4 as Functions of Rho",
            xaxis: {
              title: {
                text: 'Rho',
              },
            },
            yaxis: {
              title: {
                text: 'Hn(rho)/n^3',
              }
            }
        }

        Plotly.newPlot("first_four_plot", data, layout, {scrollZoom: false, displaylogo: false});
    },

    _replot_PSI_NDMN: function() {
        let data_title = "n = " + this.model.get("value");
        let squared_data_title = "n = " + (this.model.get("value") - 1) + " but squared actually";

        let data = [{
            "x": this.model.get('psi_ndmn')[0],
            "y": this.model.get('psi_ndmn')[1],
        }];

        let layout = {
            title: data_title,
            xaxis: {
              title: {
                text: 'Rho',
              },
            },
            yaxis: {
              title: {
                text: 'Psi_n(rho)',
              }
            }
        }

        Plotly.newPlot("PSI_NDMN", data, layout, {scrollZoom: false, displaylogo: false});

        let data_2 = [{
            "x": this.model.get('psi_ndmn')[0],
            "y": this.model.get('psi_ndmn')[2],
        }];

        let layout_2 = {
            title: squared_data_title,
            xaxis: {
              title: {
                text: 'Rho',
              },
            },
            yaxis: {
              title: {
                text: 'Psi_n(rho)^2',
              }
            }
        }

        Plotly.newPlot("PSI_NDMN_2", data_2, layout_2, {scrollZoom: false, displaylogo: false});
    },
});

module.exports = {
    HermiteWidgetModel: HermiteWidgetModel,
    HermiteWidgetView: HermiteWidgetView
};
