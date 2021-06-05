from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Int, validate, TraitError, observe
from ._frontend import module_name, module_version
import sys
import numpy as np
import math

# See js/lib/widget.js for the frontend counterpart to this file.

# make the polynomial from the matrix
def hermite(NARY):
    cols = len(NARY[0])
    rows = cols - 1     # to get the last row
    temp = ''

    temp += "H" + str(rows) + " (x) = "
    for j in range(cols - 1, -1, -1):
        if(NARY[rows][j]):     # value in the matrix not 0
            if(j == 0):     # 1st column (when x^0)
                temp += str(NARY[rows][j])
            elif(j == 1):   # 2nd column (when x^1)
                temp += str(NARY[rows][j]) + "x"
            else:
                temp += str(NARY[rows][j]) + "x^" + str(j) + " + "

    return temp

# compute matrix from the dimension given
def compute_matrix(input):
    ORDER = int(input)

    NARY = np.zeros((ORDER+1,ORDER+1))
    NARY[0,0] = 1

    if ORDER > 0:
        NARY[1,1] = 2

        # fill out the coefficient matrix using equation 4-16
        # fails if n < 1
        for k in range(ORDER+1):
            for n in range(ORDER):
                NARY[n+1,k] = 2*NARY[n,k-1] - 2*n*NARY[n-1,k]

    return NARY

# compute the data points for the polynomial graph
def compute_points(NARY):
    cols = len(NARY[0])
    last_row = cols - 1
    datapoints = []

    for x in range(100):    # taking 100 x-coordinates
        y = 0

        for j in range(cols):
            y += (NARY[last_row][j] * math.pow(x, j))

        datapoints.append([x, y])

    return datapoints


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
    value = Int(-1).tag(sync=True)
    polystring = Unicode('This is the polynomial string').tag(sync=True)

    # validator for input value
    @validate('value')
    def _valid_value(self, proposal):
        proposal_value = proposal['value']
        if proposal_value < 0 or proposal_value > 10:
            raise TraitError('Invalid integer: accepted values are 0 <= value <= 10')

        return proposal_value


# we need to adapt this into the backend of the widget at jupyterteam_widget/widget.py
# the idea is basically to replace sys.argv with the value of the widget
#
# Run this script with `python hermite.py n` where integer 5 < `n` < 264 is the dimension 
# of the array for the coefficients of each hermite polynomial order k.
# Bear in mind that the highest order hermite polynomial k and psi you will calculate is n-1.
#
# we use the physicists polynomials from here https://en.wikipedia.org/wiki/Hermite_polynomials#Definition

    @observe('value')
    def _value_changed(self, change):
        self.matrix = compute_matrix(self.value)
        self.polystring = hermite(self.matrix)
        self.datapoints = compute_points(self.matrix)