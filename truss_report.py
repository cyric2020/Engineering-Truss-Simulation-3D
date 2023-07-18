import time
import math

def prettyifyNumber(number, decimals=4):
    # Return a string representation of the number with the correct number of decimal places and add commas to the number
    return "{:,}".format(round(number, decimals))

def generateTable(columns, rows, sep="|"):
    columnLengths = [0] * len(columns)
    columnNames = columns
    for i, row in enumerate(rows):
        # the row is an array of values
        for j, value in enumerate(row):
            columnLengths[j] = max(columnLengths[j], len(str(value))) | max(columnLengths[j], len(" " + columnNames[j] + " "))
    table = ""

    # Add a seperator line
    for i, column in enumerate(columns):
        table += "-" * (columnLengths[i]+2) + sep
    table += "\n"

    # Add the column names
    for i, column in enumerate(columns):
        table += " " + column.ljust(columnLengths[i]) + " " + sep
    table += "\n"
    
    # Add the seperator
    for i, column in enumerate(columns):
        table += "-" * (columnLengths[i]+2) + sep
    table += "\n"

    # Add the rows
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            table += " " + str(value).ljust(columnLengths[j]) + " " + sep

        table += "\n"

    # Add a seperator line
    for i, column in enumerate(columns):
        table += "-" * (columnLengths[i]+2) + sep
    table += "\n"

    return table

def prettyMatrix(matrix, decimals=4):
    # Print out the matrix in a nice format
    # Get the maximum length of each column
    columnLengths = [0] * len(matrix[0])
    for i, row in enumerate(matrix):
        # the row is an array of values
        for j, value in enumerate(row):
            columnLengths[j] = max(columnLengths[j], len(str(round(value, decimals))))
    table = ""

    # Add the rows
    for i, row in enumerate(matrix):
        table += "["
        for j, value in enumerate(row):
            # Line up the numbers to the decimal point
            # get the length of ther remainder of the number after the decimal point
            remainderLength = len(str(round(value, decimals)))-len(str(round(value, decimals)).split('.')[0])-1

            numberLength = len(str(round(value, decimals)))

            # Add the spaces before the number
            table += " " * (columnLengths[j] - numberLength + remainderLength)

            # Add the number
            table += str(round(value, decimals))

            # Add the spaces after the number the inverse of the spaces before the number
            table += " " * (decimals - remainderLength) + " "

        table += "]\n"

    return table


# ------------------------------------------------------
# ------------------ Report Generator ------------------
class ReportGenerator:
    def __init__(self, truss, special="-"):
        self.truss = truss
        self.special = special
        self.report = ""
        self.report += self.generateHeader()
        self.report += self.generateTrussInfo()
        self.report += self.generateNodeInfo()
        self.report += self.generateMemberInfo()
        self.report += self.generateMaterialInfo()
        self.report += self.generateExternalForceInfo()
        self.report += self.generateFooter()
        self.report += self.diagInfo() # Diagnostic info (K, U, and F matrices)

    def generateHeader(self):
        title = f" Truss Report for \"{self.truss.Filename}\" | {time.strftime('%Y-%m-%d %H:%M:%S')} "

        header = ""
        header += self.special * len(title) + "\n"
        header += title + "\n"
        header += self.special * len(title) + "\n\n"

        return header
    
    def generateTrussInfo(self):
        info = ""
        info += f"------------------ Truss Info ------------------\n"
        info += f"Number of Nodes: {self.truss.Nodes.shape[0]}\n"
        info += f"Number of Members: {self.truss.Members.shape[0]}\n"
        info += f"Number of Materials: {len(self.truss.Materials)}\n"
        info += f"Number of External Forces: {self.truss.ExternalForces.shape[0]}\n"
        info += f"Number of Supports: {self.truss.Supports.shape[0]}\n"
        info += f"Solve Time: {round(self.truss.solveTime, 6)} seconds\n"
        info += f"------------------------------------------------\n\n"

        return info
    
    def generateNodeInfo(self):
        info = ""
        info += f"Node Info\n"
        
        nodesRows = []
        for i, node in enumerate(self.truss.Nodes):
            nodesRows.append([i, node[0], node[1], node[2], round(self.truss.U[i*3][0], 4), round(self.truss.U[i*3+1][0], 4), round(self.truss.U[i*3+2][0], 4), self.truss.Supports[i][1]])

        info += generateTable(["Node ID", "X", "Y", "Z", "Displacement X", "Displacement Y", "Displacement Z", "Support Type"], nodesRows)
        info += f"\n"

        return info
    
    def generateMemberInfo(self):
        info = ""
        info += f"Member Info\n"

        # Constants for the member table
        NODEI = 0
        NODEJ = 1
        MATERIAL = 2
        AREA = 3

        membersRows = []
        for i, member in enumerate(self.truss.Members):
            # Calculate the member length
            nodeI = self.truss.Nodes[int(member[NODEI])]
            nodeJ = self.truss.Nodes[int(member[NODEJ])]
            length = math.sqrt((nodeJ[0]-nodeI[0])**2 + (nodeJ[1]-nodeI[1])**2 + (nodeJ[2]-nodeI[2])**2)
            membersRows.append([
                i, member[NODEI], member[NODEJ], member[MATERIAL], member[AREA], round(self.truss.Forces[i][0][0], 4), round(self.truss.Stresses[i][0][0], 4), round(length, 4)
            ])

        info += generateTable(["Member ID", "Node I", "Node J", "Material", "Area", "Force", "Stress", "Length"], membersRows)
        info += f"\n"

        return info
    
    def generateMaterialInfo(self):
        info = ""
        info += f"Material Info\n"

        materialsRows = []
        for i, material in enumerate(self.truss.Materials):
            materialsRows.append([
                material, prettyifyNumber(self.truss.Materials[material]["E"]), prettyifyNumber(self.truss.Materials[material]["MaxStress"])
            ])

        info += generateTable(["Material Name", "Young's Modulus", "Max Stress"], materialsRows)
        info += f"\n"

        return info
    
    def generateExternalForceInfo(self):
        info = ""
        info += f"External Force Info\n"

        # Constants for the external force table
        X = 0
        Y = 1
        Z = 2

        externalForcesRows = []
        for i, externalForce in enumerate(self.truss.ExternalForces):
            externalForcesRows.append([
                i, prettyifyNumber(externalForce[X]), prettyifyNumber(externalForce[Y]), prettyifyNumber(externalForce[Z])
            ])

        info += generateTable(["Force ID", "X", "Y", "Z"], externalForcesRows)
        info += f"\n"

        return info
    
    def generateFooter(self):
        footer = ""
        footer += self.special * 50 + "\n"
        footer += f"Truss Report Generated by this super epik software\n"
        footer += self.special * 50 + "\n"

        return footer
    
    def diagInfo(self):
        diag = ""
        diag += f"K Matrix\n"
        diag += prettyMatrix(self.truss.K, 1)
        diag += f"\n"

        diag += f"U Matrix\n"
        diag += prettyMatrix(self.truss.U)
        diag += f"\n"

        diag += f"F Matrix\n"
        diag += prettyMatrix(self.truss.F)
        diag += f"\n"

        return diag