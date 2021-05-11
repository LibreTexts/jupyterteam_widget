# we need to adapt this into the backend of the widget at jupyterteam_widget/widget.py
# the idea is basically to replace sys.argv with the value of the widget
#
# Run this script with `python hermite.py n` where integer 5 < `n` < 264 is the dimension 
# of the array for the coefficients of each hermite polynomial order k.
# Bear in mind that the highest order hermite polynomial k and psi you will calculate is n-1.
#
# we use the physicists polynomials from here https://en.wikipedia.org/wiki/Hermite_polynomials#Definition
import sys
import numpy as np

if len(sys.argv) < 2:
    print("Please provide a dimension n for the matrix of Hermite polynomial coefficients")
    print("Exiting...")
    sys.exit()

ORDER = int(sys.argv[1])

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

# for a given rho, find the hermite polynomial of order n
def hermite(n,rho):
    coefficients = {}
    Hn = 0
    for k in range(n+1):
        coefficients[k] = NARY[n,k]
    for k in coefficients:
        Hn += coefficients[k]*rho**k
    return Hn
