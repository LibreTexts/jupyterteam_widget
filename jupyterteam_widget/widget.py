from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Int, validate, TraitError, List, observe

import numpy as np
import math

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

    x_points = List().tag(sync=True)

    y_points = List().tag(sync=True)

    # validator for input value
    @validate('value')
    def _valid_value(self, proposal):
        proposal_value = proposal['value']
        if proposal_value < 0 or proposal_value > 10:
            raise TraitError('Invalid integer: accepted values are 0 <= value <= 10')
        return proposal_value

    @observe('value')
    def _value_changed(self, change):
        temp_NARY = hermite(self.value)
        self.polystring = hermite_string(temp_NARY)
        temp_points = compute_points(temp_NARY)
        self.x_points = temp_points[0]
        self.y_points = temp_points[1]

def hermite(input): 
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

def compute_points(NARY):
    cols = len(NARY[0])
    last_row = cols - 1
    x_points = []
    y_points = []

    for x in range(100):    # taking 100 x-coordinates
        y = 0

        for j in range(cols):
            y += (NARY[last_row][j] * math.pow(x, j))

        x_points.append(x)
        y_points.append(y)

    return (x_points, y_points)

# returns a string representing the nth hermite polynomial
def hermite_string(NARY):
    rows = len(NARY[0])
    cols = rows
    rows -= 1
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

    # this code prints out all of the polynomials
    # rows = len(NARY[0])
    # cols = rows
    # temp = ""

    # for i in range(rows):
    #     temp += "H" + str(i) + " (x) = "
    #     for j in range(cols - 1, -1, -1):
    #         if(NARY[i][j]):     # value in the matrix not 0
    #             if(j == 0):     # 1st column (when x^0)
    #                 temp += str(NARY[i][j])
    #             elif(j == 1):   # 2nd column (when x^1)
    #                 temp += str(NARY[i][j]) + "x"
    #             else:
    #                 temp += str(NARY[i][j]) + "x^" + str(j) + " + "
    #     temp += "\n"

    return temp 