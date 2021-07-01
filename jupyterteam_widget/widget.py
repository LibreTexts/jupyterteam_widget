from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Int, validate, TraitError, List, observe

import numpy as np

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
    value = Int(-1).tag(sync=True)

    polystring = Unicode('').tag(sync=True)

    plot_data = List().tag(sync=True)

    # validator for input value
    @validate('value')
    def _valid_value(self, proposal):
        proposal_value = proposal['value']
        if proposal_value < 0 or proposal_value > 10:
            raise TraitError('Invalid integer: accepted values are 0 <= value <= 10')
        return proposal_value

    @observe('value')
    def _value_changed(self, change):
        N = self.value
        temp_matrix = hermite_array(N)
        self.polystring = hermite_string(temp_matrix)

        x_axis = np.linspace(-5,5,10**3)
        y_axis = []

        for x in x_axis:
            y_axis.append(hermite_polynomial(N,x))

        plot_axes = [x_axis,y_axis]
        self.plot_data = plot_axes

# returns a square array of hermite coefficients up to N
def hermite_array(N):

    # dimension of array is 1 greater than the requested polynomial
    # because polynomials start at order N = 0
    matrix = np.zeros((N+1,N+1))

    # initial entry, necessary when N = 0
    matrix[0,0] = 1

    if N > 0:
        matrix[1,1] = 2

        # fill out the coefficient matrix according to a recursive pattern
        for k in range(N+1):
            for n in range(N):
                matrix[n+1,k] = 2*matrix[n,k-1] - 2*n*matrix[n-1,k]

    return matrix

# for a given value x, find the hermite polynomial HN of order N
def hermite_polynomial(N,x):
    matrix = hermite_array(N)
    coefficients = {}
    HN = 0

    # grab a row of values from matrix
    for k in range(N+1):
        coefficients[k] = matrix[N,k]

    # multiply x by each value k in the row and raise it
    # by its key k (position in the row).
    # sum them to complete the polynomial
    for k in coefficients:
        HN += coefficients[k]*x**k

    return HN

# returns a string representing the nth hermite polynomial
def hermite_string(matrix):
    rows = len(matrix[0])
    cols = rows
    rows -= 1
    temp = ''

    temp += "H" + str(rows) + " (x) = "
    for j in range(cols - 1, -1, -1):
        if matrix[rows][j]:     # value in the matrix not 0
            if j == 0:     # 1st column (when x^0)
                temp += str(matrix[rows][j])
            elif j == 1:   # 2nd column (when x^1)
                temp += str(matrix[rows][j]) + "x"
            else:
                temp += str(matrix[rows][j]) + "x^" + str(j) + " + "

    return temp
