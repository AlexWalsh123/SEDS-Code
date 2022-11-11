from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
from MainWindow import MainWindow
import sys 
from FlightComputerSimulator import Simulator

app = QtWidgets.QApplication(sys.argv)
Window = MainWindow()
sim = Simulator()

Window.setCentralWidget(Window.graphWidget)
Window.show()
Window.setWindowTitle("Ground Control")

sys.exit(app.exec())


