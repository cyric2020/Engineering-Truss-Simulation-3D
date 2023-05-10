from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import truss
import random

# Set the random seed
random.seed(111)

# Load the truss
bridge = truss.Truss()
bridge.loadTruss('trusses/warren_rise.yaml')

# Solve the truss
bridge.solveTruss()

# Get the forces
forces = bridge.Forces
data = np.array([abs(force[0][0]) for force in forces])


# Use mean squared error to find the best number of clusters
from sklearn.metrics import mean_squared_error

# Create a list of the mean squared errors
errors = []

# # Loop through each number of clusters
# for n_clusters in range(1, 10):
#     # Perform k-means clustering with n_clusters clusters
#     kmeans = KMeans(n_clusters=n_clusters).fit(data.reshape(-1,1))

#     # Get the cluster labels for each data point
#     labels = kmeans.labels_

#     # Get the cluster centers
#     centers = kmeans.cluster_centers_

#     # Get the mean squared error
#     error = mean_squared_error(data, centers[labels])

#     # Add the error to the list
#     errors.append(error)

# # Plot the mean squared errors
# plt.plot(range(1, 10), errors)

# # Show the plot
# plt.show()
# exit()

kn = 6

# Perform k-means clustering with 3 clusters
kmeans = KMeans(n_clusters=kn, random_state=111).fit(data.reshape(-1,1))

# Get the cluster labels for each data point
labels = kmeans.labels_

# Print out the data points in each cluster
# for cluster in range(3):
#     print(f'Cluster {cluster}:')
#     for data_point, label in zip(data, labels):
#         if label == cluster:
#             print(data_point)
#     print()

# Print the max force in each cluster
for cluster in range(kn):
    print(f'Cluster {cluster}:')
    maxForce = max([data_point for data_point, label in zip(data, labels) if label == cluster])
    # print(maxForce, maxForce/353333333)
    print(maxForce, f'{maxForce/353333333:.20f}')
    print()

# Print the member ids in each cluster
for cluster in range(kn):
    print(f'Cluster {cluster}:')
    for member_index, label in enumerate(labels):
        if label == cluster:
            print(member_index, end=', ')
    print()

colormap = plt.cm.jet # https://matplotlib.org/stable/tutorials/colors/colormaps.html 
# Plot the bridge in 3D with the clusters as different colors
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Loop through all the clusters getting the members in each label
for cluster in range(kn):
    members = [member for member, label in zip(bridge.Members, labels) if label == cluster]

    # Loop through each member
    for member in members:
        # Get the member nodes
        node1 = bridge.Nodes[int(member[0])]
        node2 = bridge.Nodes[int(member[1])]

        # Get the node coordinates
        x1, y1, z1 = node1
        x2, y2, z2 = node2

        # Plot the member using the colormap
        ax.plot([x1, x2], [y1, y2], [z1, z2], color=colormap(cluster/4))

    # Add that cluster to the legend
    ax.scatter([], [], [], color=colormap(cluster/4), label=f'Cluster {cluster}')

# Add the legend
ax.legend()

# Show the plot for fig
max_range = np.array([bridge.Nodes[:,0].max()-bridge.Nodes[:,0].min(), bridge.Nodes[:,1].max()-bridge.Nodes[:,1].min(), bridge.Nodes[:,2].max()-bridge.Nodes[:,2].min()]).max() / 2.0

# get the mid point of the axes
mid_x = (bridge.Nodes[:,0].max()+bridge.Nodes[:,0].min()) * 0.5
mid_y = (bridge.Nodes[:,1].max()+bridge.Nodes[:,1].min()) * 0.5
mid_z = (bridge.Nodes[:,2].max()+bridge.Nodes[:,2].min()) * 0.5

# set the axes limits
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

# Show the plot
plt.show()

# Generate table information
# Columns: Member Index (Index), start node, end node, force, stress, area, cluster
tablecsv = 'Index, Start Node, End Node, Force, Stress, Area, Cluster No., Max Stress\n'
for memberId, member in enumerate(bridge.Members):
    startNode, endNode, Material, Area = member
    startNode, endNode, Material, Area = int(startNode), int(endNode), bridge.Materials[Material], float(Area)

    # Get the force
    force = bridge.Forces[memberId][0][0]

    # Get the stress
    stress = bridge.Stresses[memberId][0][0]

    # Get the cluster
    cluster = labels[memberId]

    # Get the max stress from the material
    maxStress = Material['MaxStress']

    # Add the row to the table
    tablecsv += f'{memberId},{startNode},{endNode},{force},{stress},{Area},{cluster},{maxStress}\n'

# Write the table to a csv file
with open('table.csv', 'w') as f:
    f.write(tablecsv)
    f.close()

exit()

# Plot the data points
# plt.scatter(data, np.zeros_like(data), c=labels, cmap=colormap)
for cluster in range(kn):
    plt.scatter(data[labels == cluster], np.zeros_like(data[labels == cluster]), color=colormap(cluster / kn))

# Plot the cluster centers
# plt.scatter(kmeans.cluster_centers_, np.zeros_like(kmeans.cluster_centers_), c='red', marker='x', s=100)

# Set the x label
plt.xlabel('Absolute Force (N)')

# Increase the padding on the bottom
plt.subplots_adjust(bottom=0.5)

# Create the legend with the different colors of the clusters
for cluster in range(kn):
    # plt.scatter([], [], c=f'C{cluster}', label=f'Cluster {cluster}')
    # Get the correct color from the cmap
    color = colormap(cluster / kn)
    plt.scatter([], [], color=color, label=f'Cluster {cluster + 1}')

# Show the legend
plt.legend(loc='upper center', ncol=kn, bbox_to_anchor=(0.5, 0.4))

# Show the plot
plt.show()