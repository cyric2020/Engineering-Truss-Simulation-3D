""" Port of truss_materials.py (2d FEA truss solver) to 3d.

Author: Cyric

https://people.duke.edu/~hpgavin/cee421/truss-3d.pdf (carrying)
"""

import numpy as np
import yaml
import time

class Truss:
    def __init__(self):
        """Initialize the truss object."""
        self.solveTime = 0
        pass

    def loadTruss(self, filename):
        """Load a truss from a file."""
        # Load the data from the file
        with open(filename, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        # Get the nodes
        self.Nodes = np.array(data['Joints'])

        # Get the members
        self.Members = np.array(data['Members'])

        # Get the materials
        self.Materials = data['Materials']

        # Get the external forces
        self.ExternalForces = np.array(data['ExternalForces'])

        # Get the supports
        self.Supports = np.array(data['Supports'])

        self.Filename = filename

    def solveTruss(self):
        """Solve the truss."""
        
        # Start the timer
        start = time.time()

        # Create the global stiffness matrix
        n_nodes = self.Nodes.shape[0]
        n_dofs = n_nodes * 3
        K = np.zeros((n_dofs, n_dofs))

        # Loop over the elements and generate the local stiffness matrices
        stiffnessMatrices = []
        for member in self.Members:
            # Get the member information
            node1, node2, Material, Area = member
            # Convert the types
            node1, node2, Material, Area = int(node1), int(node2), str(Material), float(Area)

            # Get the young's modulus
            E = float(self.Materials[Material]['E'])

            # Get the node coordinates
            x1, y1, z1 = self.Nodes[node1]
            x2, y2, z2 = self.Nodes[node2]

            # Calculate the length of the member
            L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

            # Calculate the cosines for each direction
            cos_x = (x2 - x1) / L
            cos_y = (y2 - y1) / L
            cos_z = (z2 - z1) / L

            # Precalculate all the terms to save time
            cos_x_2 = cos_x**2
            cos_y_2 = cos_y**2
            cos_z_2 = cos_z**2
            cos_x_cos_y = cos_x * cos_y
            cos_x_cos_z = cos_x * cos_z
            cos_y_cos_z = cos_y * cos_z

            # Calculate the local stiffness matrix
            k = E * Area / L * np.array([
                [cos_x_2, cos_x_cos_y, cos_x_cos_z, -cos_x_2, -cos_x_cos_y, -cos_x_cos_z],
                [cos_x_cos_y, cos_y_2, cos_y_cos_z, -cos_x_cos_y, -cos_y_2, -cos_y_cos_z],
                [cos_x_cos_z, cos_y_cos_z, cos_z_2, -cos_x_cos_z, -cos_y_cos_z, -cos_z_2],
                [-cos_x_2, -cos_x_cos_y, -cos_x_cos_z, cos_x_2, cos_x_cos_y, cos_x_cos_z],
                [-cos_x_cos_y, -cos_y_2, -cos_y_cos_z, cos_x_cos_y, cos_y_2, cos_y_cos_z],
                [-cos_x_cos_z, -cos_y_cos_z, -cos_z_2, cos_x_cos_z, cos_y_cos_z, cos_z_2]
            ])

            # Add the local stiffness matrix to the list
            stiffnessMatrices.append(k)

            # Get the coordinates of the degrees of freedom
            dofs = [3 * node1, 3 * node1 + 1, 3 * node1 + 2, 3 * node2, 3 * node2 + 1, 3 * node2 + 2]

            # Add the local stiffness matrix to the global stiffness matrix
            K[np.ix_(dofs, dofs)] += k
        
        # Save the K matrix for later
        self.K = K

        # Finite Element Equation
        # [K]{u} = {F}

        # Assemble the global external forces vector F
        F = np.zeros((n_dofs, 1))
        for i, force in enumerate(self.ExternalForces):
            # Get the node id
            node_id = i

            # Apply the force to the global forces vector
            dofs = [3 * node_id, 3 * node_id + 1, 3 * node_id + 2]
            F[dofs, 0] = force

        # Save the F vector for later
        self.F = F

        # Add boundary conditions to the global stiffness matrix
        # Remove the rows and columns of the global stiffness matrix that correspond to the boundary conditions
        removedOffset = 0
        removedDofs = []

        # Create temporary variables to hold the boundary conditions
        K_solve = K.copy()
        F_solve = F.copy()

        for support in self.Supports:
            # Get the node id and support type
            node_id, support_type = support

            # Convert the types
            node_id = int(node_id)

            if support_type == "PIN":
                # Get the coordinates of the degrees of freedom
                dofs = np.array([3 * node_id, 3 * node_id + 1, 3 * node_id + 2])
            elif support_type == "ROLLER_X":
                # Get the coordinates of the degrees of freedom
                dofs = np.array([3 * node_id + 1, 3 * node_id + 2])
            elif support_type == "ROLLER_Y":
                # Get the coordinates of the degrees of freedom
                dofs = np.array([3 * node_id, 3 * node_id + 2])
            elif support_type == "ROLLER_Z":
                # Get the coordinates of the degrees of freedom
                dofs = np.array([3 * node_id, 3 * node_id + 1])
            else:
                continue

            # Remove the rows and columns
            K_solve = np.delete(K_solve, dofs - removedOffset, axis=0)
            K_solve = np.delete(K_solve, dofs - removedOffset, axis=1)

            # Remove the external forces
            F_solve = np.delete(F_solve, dofs - removedOffset, axis=0)

            # Update the offset
            removedOffset += len(dofs)

            # Add the dofs to the removed dofs list
            removedDofs.append(dofs)

        # Check to see if the matrix is singular
        if np.linalg.det(K_solve) == 0:
            raise Exception("The matrix is singular.")
        
        # Solve for the nodal displacements U
        U_solve = np.linalg.solve(K_solve, F_solve)

        # Create the global displacements vector U
        U = np.zeros((n_dofs, 1))
        U[np.setdiff1d(np.arange(n_dofs), removedDofs)] = U_solve

        # Save the U vector for later
        self.U = U

        # Calculate the stresses and internal forces in each member
        stresses = []
        forces = []
        for o, member in enumerate(self.Members):
            # Get the member information
            node1, node2, Material, Area = member

            # Convert the types
            node1, node2, Material, Area = int(node1), int(node2), str(Material), float(Area)

            # Get the young's modulus
            E = float(self.Materials[Material]['E'])

            # Calculate the length of the member
            x1, y1, z1 = self.Nodes[node1]
            x2, y2, z2 = self.Nodes[node2]
            L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

            # Calculate the cosines for each direction
            cos_x = (x2 - x1) / L
            cos_y = (y2 - y1) / L
            cos_z = (z2 - z1) / L

            # Get the nodal displacements for the element
            u = np.array([self.U[3 * node1], self.U[3 * node1 + 1], self.U[3 * node1 + 2], self.U[3 * node2], self.U[3 * node2 + 1], self.U[3 * node2 + 2]])

            # Calculate the stress and force
            stress = E / L * np.array([
                [cos_x, cos_y, cos_z, -cos_x, -cos_y, -cos_z]
            ]).dot(u)
            force = Area * stress

            # Add the stress and force to the list
            stresses.append(stress)
            forces.append(force)

        # Save the stresses and forces for later
        self.Stresses = stresses
        self.Forces = forces