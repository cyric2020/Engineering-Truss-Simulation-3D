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

# Apply precomputed clustered areas
clusters = [
    [7, 10, 11, 14, 27, 30, 35, 39, 40, 44, 50, 53, 62, 63, 70, 71, 78, 79, 86, 87],
    [36, 37, 38, 41, 42, 43, 59, 66, 67, 74, 75, 82, 83, 90],
    [0, 2, 20, 22, 25, 28, 52, 55],
    [1, 3, 19, 21, 26, 29, 51, 54, 61, 64, 69, 72, 77, 80, 85, 88],
    [4, 5, 6, 15, 16, 17, 18, 23, 24, 31, 32, 33, 34, 45, 46, 47, 48, 49, 56, 57, 58, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117],
    [8, 9, 12, 13, 60, 65, 68, 73, 76, 81, 84, 89]
]
clusterAreas = [
    0.0001,
    0.000324,
    0.000441,
    0.000144,
    0.000009,
    0.000225
]

for clusterIndex, (cluster, clusterArea) in enumerate(zip(clusters, clusterAreas)):
    # Also save each cluster to a new members and joints csv
    members = ''
    joints = ''
    for memberId in cluster:
        bridge.Members[memberId][3] = clusterArea
        members += f'{bridge.Members[memberId][0]}, {bridge.Members[memberId][1]}\n'
    
    for joint in bridge.Nodes:
        x, y, z = joint
        x *= 100
        y *= 100
        z *= 100
        joints += f'{x}, {z}, {y}\n'

    with open(f'clusters/joints_{clusterIndex}.csv', 'w') as f:
        f.write(joints)
    with open(f'clusters/members_{clusterIndex}.csv', 'w') as f:
        f.write(members)

bridge.applySelfWeight()

# Apply wind udl
# windUdlNodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 18, 19, 20, 24, 25, 26, 27, 28, 29, 36, 37, 38]
# windForce = -2_908.54

# for node in windUdlNodes:
#     bridge.ExternalForces[node][1] += windForce

bridge.solveTruss()

# Save the report
report = ReportGenerator(bridge).report
with open('report.txt', 'w') as f:
    f.write(report)

# print(bridge.U)

# print(bridge.Forces)

trussRenderer = ViewTruss()

if bridge.fails(fos=1.5):
# if bridge.fails(fos=5):
# if bridge.fails(fos=0.00000000001):
    print('Truss failed')
    # trussRenderer.showFailedMembers(bridge)
    trussRenderer.showForcesGradient(bridge)
else:
    trussRenderer.showTruss(bridge, NodeLabels=True)
    # trussRenderer.showTrussDisplacements(bridge, bridge.U, bridge.Forces, MemberForces=False, ExternalForces=True)
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