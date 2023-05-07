from truss import Truss
from truss_visualiser import ViewTruss
from truss_report import ReportGenerator
from matplotlib import pyplot as plt

bridge = Truss()

# bridge.loadTruss('trusses/smol.yaml')
# bridge.loadTruss('trusses/pyramid.yaml')
# bridge.loadTruss('trusses/line.yaml')
# bridge.loadTruss('trusses/big.yaml')
# bridge.loadTruss('trusses/big_other.yaml')

bridge.loadTruss('trusses/warren_rise.yaml')

# trussRenderer = ViewTruss()
# trussRenderer.cube_full()
# trussRenderer.showTruss(bridge, NodeLabels=True)
# trussRenderer.show(bridge)
# exit()

print(round(bridge.calculateSelfWeight(), 2), "Kg")

bridge.applySelfWeight()

bridge.solveTruss()

# Save the report
report = ReportGenerator(bridge).report
with open('report.txt', 'w') as f:
    f.write(report)


# SMART_AREA = False
# ROUND = True
# if SMART_AREA:
#     # Loop through each member in the truss
#     for member_index, member in enumerate(bridge.Members):
#         # Get the force, stress, area and material
#         force = bridge.Forces[member_index]
#         stress = bridge.Stresses[member_index]
#         area = float(member[3])
#         material = bridge.Materials[member[2]]

#         # Calculate the new area
#         new_area = area * (1 + stress / material['MaxStress'])[0][0]

#         print(new_area)

#         # Set the new area
#         bridge.Members[member_index][3] = round(new_area, 2) + 0.01

bridge.solveTruss()

# print(bridge.U)

# print(bridge.Forces)

trussRenderer = ViewTruss()

# if bridge.fails(fos=1.5):
if bridge.fails(fos=5):
# if bridge.fails(fos=0.00000000001):
    print('Truss failed')
    # trussRenderer.showFailedMembers(bridge)
    trussRenderer.showForcesGradient(bridge)
else:
    # trussRenderer.showTruss(bridge, NodeLabels=False)
    trussRenderer.showTrussDisplacements(bridge, bridge.U, bridge.Forces, MemberForces=False, ExternalForces=False)
    pass

# Create a csv file for the member forces
membersCSV = 'Index, Start Node, End Node, Force, Stress, Area, Max Stress\n'
for member_index, member in enumerate(bridge.Members):
    # Get the member index, start node, end node, force, stress, area, and max stress
    start_node = member[0]
    end_node = member[1]
    force = bridge.Forces[member_index][0][0]
    stress = bridge.Stresses[member_index][0][0]
    area = member[3]
    material = bridge.Materials[member[2]]

    # Calculate the max stress
    max_stress = material['MaxStress']

    # Add the member to the csv
    membersCSV += f'{member_index},{start_node},{end_node},{force},{stress},{area},{max_stress}\n'

# Save the csv
with open('member_table.csv', 'w') as f:
    f.write(membersCSV)

trussRenderer.cube_full()
trussRenderer.show(bridge)