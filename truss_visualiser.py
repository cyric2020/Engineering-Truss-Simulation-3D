from matplotlib import pyplot as plt
import numpy as np

class ViewTruss:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def showTruss(self, truss, NodeLabels=False, MemberLabels=False):
        # Show all the nodes
        # ax.scatter(truss.Nodes[:,0], truss.Nodes[:,1], truss.Nodes[:,2])
        # Loop through all the nodes, if the node is a PIN then plot it as a red dot, if it is a ROLLER then plot it as a blue dot else plot it as a green dot
        for node_index, node in enumerate(truss.Nodes):
            # Get the node information
            x, y, z, = node

            # Get the support
            support = truss.Supports[node_index][1]

            # Plot the node
            if support == 'PIN':
                self.ax.scatter(x, y, z, c='r')
            elif support == 'ROLLER':
                self.ax.scatter(x, y, z, c='b')
            else:
                self.ax.scatter(x, y, z, c='g') 

            if NodeLabels:
                # Add the node label with a white background
                self.ax.text(x, y, z, str(node_index), color='k', backgroundcolor='w')
        
        # Show all the members
        for member in truss.Members:
            # Get the member information
            node1, node2, Material, Area = member
            # Convert the types
            node1, node2, Material, Area = int(node1), int(node2), str(Material), float(Area)

            # Get the node coordinates
            x1, y1, z1 = truss.Nodes[node1]
            x2, y2, z2 = truss.Nodes[node2]

            # Plot the member
            self.ax.plot([x1, x2], [y1, y2], [z1, z2], 'k:')

    def showTrussDisplacements(self, truss, displacements, forces, MemberLabels=False, MemberForces=False, ExternalForces=False):
        # Loop through all the nodes and move them by the displacements
        for node_index, node in enumerate(truss.Nodes):
            # Get the node information
            x, y, z, = node

            # Get the node displacements
            dx, dy, dz = displacements[node_index*3], displacements[node_index*3+1], displacements[node_index*3+2]

            # Plot the node
            self.ax.scatter(x+dx, y+dy, z+dz, c='m')

        # Draw the members with their new positions and colour them according to the force (red for compression, blue for tension)
        # Get the minimum and maximum absolute force
        minForce = abs(min(forces, key=abs))[0][0]
        maxForce = abs(max(forces, key=abs))[0][0]
        for member_index, member in enumerate(truss.Members):
            # Get the member information
            node1, node2, Material, Area = member
            # Convert the types
            node1, node2, Material, Area = int(node1), int(node2), str(Material), float(Area)

            # Get the node coordinates
            x1, y1, z1 = truss.Nodes[node1]
            x2, y2, z2 = truss.Nodes[node2]

            # Get the node displacements
            dx1, dy1, dz1 = displacements[node1*3][0], displacements[node1*3+1][0], displacements[node1*3+2][0]
            dx2, dy2, dz2 = displacements[node2*3][0], displacements[node2*3+1][0], displacements[node2*3+2][0]

            # Get the member force
            force = forces[member_index][0][0]

            # Calculate the opacity of the member based on the force
            opacity = abs(force) / maxForce
            # opacity = 1

            # Plot the member
            if force < 0:
                color = (0, 0, 1 * opacity)
            elif force > 0:
                color = (1 * opacity, (1-opacity)/2, (1-opacity)/2)
            else:
                color = (0, 1, 0)
                
            self.ax.plot([x1+dx1, x2+dx2], [y1+dy1, y2+dy2], [z1+dz1, z2+dz2], color=color)

            if MemberLabels:
                # Add the member label with a white background
                self.ax.text((x1+dx1+x2+dx2)/2, (y1+dy1+y2+dy2)/2, (z1+dz1+z2+dz2)/2, str(member_index), color='k', backgroundcolor='w')

            if MemberForces:
                # Add the member force with a lavender background
                forceRounded = round(force, 4)
                self.ax.text((x1+dx1+x2+dx2)/2, (y1+dy1+y2+dy2)/2, (z1+dz1+z2+dz2)/2, str(forceRounded), color='k', backgroundcolor='lavender', horizontalalignment='center', verticalalignment='center', transform=self.ax.transData)

        # Show all the external forces
        if ExternalForces:
            for i, force in enumerate(truss.ExternalForces):
                x, y, z, = force

                # Get the node that the force is applied to
                node = truss.Nodes[i]

                # If the force is not zero then plot it as an arrow in the direction of the force pointing towards the node.
                arrowLength = 0.1
                arrowHead = 0.01
                if x != 0:
                    self.ax.quiver(node[0], node[1], node[2], arrowLength, 0, 0, arrow_length_ratio=arrowHead, color='r')
                    self.ax.text(node[0]+arrowLength, node[1], node[2], str(x), color='k', backgroundcolor='w', horizontalalignment='center', verticalalignment='bottom', transform=self.ax.transData)
                if y != 0:
                    self.ax.quiver(node[0], node[1], node[2], 0, arrowLength, 0, arrow_length_ratio=arrowHead, color='r')
                    self.ax.text(node[0], node[1]+arrowLength, node[2], str(y), color='k', backgroundcolor='w', horizontalalignment='center', verticalalignment='bottom', transform=self.ax.transData)
                if z != 0:
                    self.ax.quiver(node[0], node[1], node[2], 0, 0, arrowLength, arrow_length_ratio=arrowHead, color='r')
                    self.ax.text(node[0], node[1], node[2]+arrowLength, str(z), color='k', backgroundcolor='w', horizontalalignment='center', verticalalignment='bottom', transform=self.ax.transData)

    def cube_full(self):
        # Make the top bottom left and right margins 0
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

    def show(self, truss):
        # set equal limits for all axes
        # get the maximum range of the axes
        max_range = np.array([truss.Nodes[:,0].max()-truss.Nodes[:,0].min(), truss.Nodes[:,1].max()-truss.Nodes[:,1].min(), truss.Nodes[:,2].max()-truss.Nodes[:,2].min()]).max() / 2.0

        # get the mid point of the axes
        mid_x = (truss.Nodes[:,0].max()+truss.Nodes[:,0].min()) * 0.5
        mid_y = (truss.Nodes[:,1].max()+truss.Nodes[:,1].min()) * 0.5
        mid_z = (truss.Nodes[:,2].max()+truss.Nodes[:,2].min()) * 0.5

        # set the axes limits
        self.ax.set_xlim(mid_x - max_range, mid_x + max_range)
        self.ax.set_ylim(mid_y - max_range, mid_y + max_range)
        self.ax.set_zlim(mid_z - max_range, mid_z + max_range)

        # Show the plot
        plt.show()