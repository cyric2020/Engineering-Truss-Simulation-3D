from truss import Truss
from truss_visualiser import ViewTruss
from truss_report import ReportGenerator
from matplotlib import pyplot as plt
import os

truss = Truss()

truss.loadTruss('code_test.yaml')

# Solve the truss
truss.solveTruss()

print(truss.K)
print(truss.F)
# Print the local stiffness matrices
