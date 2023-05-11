import yaml
from truss import Truss
from truss_visualiser import ViewTruss
import matplotlib.pyplot as plt
import random

FILENAME = 'trusses/warren_rise.yaml'

# Load the truss
truss = Truss()

truss.loadTruss(FILENAME)

# Set all external forces to 0
for externalForce in truss.ExternalForces:
    externalForce[2] = 0

# Divide all node coordinates by 40
for node in truss.Nodes:
    node[0] /= 40
    node[1] /= 40
    node[2] /= 40

# Set all member materials to Plastic
for member in truss.Members:
    member[2] = 'Plastic'
    member[3] = '0.000036'

# Gradually increase the force on the center two nodes
maxForce = 388.36423206
i = 0
nodes = [7, 11]

forceChart = []
displacementChart = []
i_s = []

truss.solveTruss()
while not truss.fails():
    i += 1
    i_s.append(i)
    maxForce += 0.00000001
    for node in nodes:
        truss.ExternalForces[node][2] = -maxForce
    truss.solveTruss()

    # Get the y force and displacement at the first node
    forceChart.append(maxForce)
    # print(truss.U[nodes[0]*2][0])
    displacementChart.append(abs(truss.U[nodes[0]*2][0]))

    print(f'Testing Max Force: {maxForce}', end='\r')

print(f'Max force: {maxForce}')

# Plot the lines with lables against i_s
# plt.plot(i_s, forceChart, label='Force')
# plt.plot(i_s, displacementChart, label='Displacement')

# Plot the lines with different scales
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Iteration')
ax1.set_ylabel('Force', color=color)
ax1.plot(i_s, forceChart, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Displacement', color=color)
ax2.plot(i_s, displacementChart, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()

# plt.legend()

plt.show()

# trussRenderer = ViewTruss()

# trussRenderer.showTrussDisplacements(truss, truss.U, truss.Forces, MemberForces=False, ExternalForces=True)

# trussRenderer.cube_full()
# trussRenderer.show(truss)