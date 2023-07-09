from truss import Truss
from truss_visualiser import ViewTruss
from truss_report import ReportGenerator
from matplotlib import pyplot as plt

panel = Truss()

panel.loadTruss('solar_panel_frames/1.yaml')

# Show the truss
view = ViewTruss()
view.showTruss(panel, NodeLabels=True)

plt.show()