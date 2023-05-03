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

bridge.solveTruss()

# Save the report
report = ReportGenerator(bridge).report
with open('report.txt', 'w') as f:
    f.write(report)


# print(bridge.U)

# print(bridge.Forces)

trussRenderer = ViewTruss()

trussRenderer.showFailedMembers(bridge)

# trussRenderer.showTruss(bridge, NodeLabels=False)
# trussRenderer.showTrussDisplacements(bridge, bridge.U, bridge.Forces, MemberForces=False, ExternalForces=False)

trussRenderer.cube_full()
trussRenderer.show(bridge)