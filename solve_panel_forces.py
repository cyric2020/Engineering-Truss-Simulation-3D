from truss import Truss
from truss_visualiser import ViewTruss
from truss_report import ReportGenerator
from matplotlib import pyplot as plt
import os

panel = Truss()

# Force scenarios
beginning = [5_400, 0, -9_650]
perpendicular = [-27.4, 51_000, -76]

def test_panel(panel, forces):
    # Subtract 1177.4N from the vertical force to account for the weight of the panel
    # forces[2] -= 1177.4

    panel.ExternalForces[1] = forces

    # Solve the truss
    panel.solveTruss()

    # Return the member forces
    member_forces = panel.Forces

    # The member forces are an array of numpy arrays
    # Convert them to a list of floats
    for i in range(len(member_forces)):
        member_forces[i] = int(round(member_forces[i][0][0], 0))
    # return panel.Forces
    return member_forces

# # Loop through every file in the 'solar_panel_frames' directory
# for file in os.listdir('solar_panel_frames'):
#     # Load the truss
#     tmp_panel = Truss()
#     tmp_panel.loadTruss(f'solar_panel_frames/{file}')

#     beginning_forces = test_panel(tmp_panel, beginning)
#     perpendicular_forces = test_panel(tmp_panel, perpendicular)

#     # Print the results
#     print(f'File: {file}')
#     print(f'Beginning Forces: {beginning_forces}')
#     print(f'Perpendicular Forces: {perpendicular_forces}')
#     print('')


panel.loadTruss('solar_panel_frames/6m1m.yaml')

# [+south, +east, +up]
# Forces = [5_400, 0, -9_650] # Beginning Configuration
Forces = [-27.4, 51_000, -76] # Perpendicular Configuration

# Subtract 1177.4N from the vertical force to account for the weight of the panel
Forces[2] -= 1177.4

panel.ExternalForces[1] = Forces

# Solve the truss
panel.solveTruss()

# Show the truss
view = ViewTruss()
# view.showTruss(panel, NodeLabels=True)
# view.showForcesGradient(panel)
# view.showTrussDisplacements(panel, panel.U, panel.Forces, MemberForces=False, ExternalForces=True)
view.showTrussDisplacements(panel, panel.U, panel.Forces, MemberForces=True, ExternalForces=False)

# view.cube_full()
# view.show(panel)

# Print out the report
report = ReportGenerator(panel)
print(report.report)