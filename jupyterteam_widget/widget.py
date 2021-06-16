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

    first_four = List().tag(sync=True)

    psi_ndmn = List().tag(sync=True)

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

        INTERVALS = 10**3

        # construct x and y values for the first four pot
        rhoAxis = np.linspace(0,2.5,INTERVALS)
        tempthing = []

        for i in range(5):
            tempthing.append([])
        for x in rhoAxis:
            tempthing[0].append(x)
            tempthing[1].append(singleHermite(1,x))
            tempthing[2].append(singleHermite(2,x)/8)
            tempthing[3].append(singleHermite(3,x)/27)
            tempthing[4].append(singleHermite(4,x)/64)

        self.first_four = tempthing

        if self.value > 0:
            # values for the second plot
            rhoPsi = np.linspace(-5,5,INTERVALS)
            tempthing = []
            tempthing.append([])
            n = self.value
            psi = []
            for x in rhoPsi:
                tempthing[0].append(x)
                Hn = singleHermite(n,x)
                psiCoefficient = math.e**(-x**2/2)/(2**n*math.factorial(n)*(math.pi)**(1/2))**(1/2)
                psi.append(psiCoefficient*Hn)        
            tempthing.append(psi)

            # values for the third plot
            psi = []
            for x in rhoPsi:
                Hn = singleHermite(n-1,x)
                psiCoefficient = math.e**(-x**2/2)/(2**n*math.factorial(n)*(math.pi)**(1/2))**(1/2)
                psi.append((psiCoefficient*Hn)**2)        
            tempthing.append(psi)

            self.psi_ndmn = tempthing
        
# returns NARY thing up to n = input
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

    return temp 

# for a given rho, find the hermite polynomial of order n
def singleHermite(n,rho):
    NARY = hermite(n)
    coefficients = {}
    Hn = 0
    for k in range(n+1):
        coefficients[k] = NARY[n,k]
    for k in coefficients:
        Hn += coefficients[k]*rho**k
    return Hn