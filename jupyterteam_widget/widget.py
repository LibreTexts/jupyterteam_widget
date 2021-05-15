from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Int, validate, TraitError

from ._frontend import module_name, module_version

import sys
import numpy as np

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

    # validator for input value
    @validate('value')
    def _valid_value(self, proposal):
        proposal_value = proposal['value']
        if proposal_value < 0 or proposal_value > 10:
            raise TraitError('Invalid integer: accepted values are 0 <= value <= 10')

        # compute the matrix if the value entered is valid
        compute_matrix(proposal_value)



# we need to adapt this into the backend of the widget at jupyterteam_widget/widget.py
# the idea is basically to replace sys.argv with the value of the widget
#
# Run this script with `python hermite.py n` where integer 5 < `n` < 264 is the dimension 
# of the array for the coefficients of each hermite polynomial order k.
# Bear in mind that the highest order hermite polynomial k and psi you will calculate is n-1.
#
# we use the physicists polynomials from here https://en.wikipedia.org/wiki/Hermite_polynomials#Definition

def compute_matrix(self):
    ORDER = int(self)

    NARY = np.zeros((ORDER+1,ORDER+1))
    NARY[0,0] = 1

    if ORDER > 0:
        NARY[1,1] = 2

        # fill out the coefficient matrix using equation 4-16
        # fails if n < 1
        for k in range(ORDER+1):
            for n in range(ORDER):
                NARY[n+1,k] = 2*NARY[n,k-1] - 2*n*NARY[n-1,k]

    print(NARY)
    hermite(NARY)


# make the polynomial from the matrix
def hermite(NARY):
    rows = len(NARY[0])
    cols = rows
    
    for i in range(rows):
        temp = "H" + str(i) + " (x) = "
        for j in range(cols - 1, -1, -1):
            if(NARY[i][j]):     # value in the matrix not 0
                if(j == 0):     # 1st column (when x^0)
                    temp += str(NARY[i][j])
                elif(j == 1):   # 2nd column (when x^1)
                    temp += str(NARY[i][j]) + "x"
                else:
                    temp += str(NARY[i][j]) + "x^" + str(j) + " + "

        print(temp)