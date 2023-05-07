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


# Perform k-means clustering with 3 clusters
kmeans = KMeans(n_clusters=4).fit(data.reshape(-1,1))

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
for cluster in range(4):
    print(f'Cluster {cluster}:')
    print(max([data_point for data_point, label in zip(data, labels) if label == cluster]))
    print()

# Print the member ids in each cluster
for cluster in range(4):
    print(f'Cluster {cluster}:')
    for member_index, label in enumerate(labels):
        if label == cluster:
            print(member_index, end=', ')
    print()

# Plot the data points
plt.scatter(data, np.zeros_like(data), c=labels, cmap='viridis')

# Plot the cluster centers
plt.scatter(kmeans.cluster_centers_, np.zeros_like(kmeans.cluster_centers_), c='red', marker='x', s=100)

# Set the x label
plt.xlabel('Absolute Force (N)')

# Increase the padding on the bottom
plt.subplots_adjust(bottom=0.5)

# Show the plot
plt.show()