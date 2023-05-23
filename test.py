import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QWidget
import sys


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100,_3D=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
       
        self.axes = self.fig.add_subplot()
        self.axes.plot([1,2,3],[3,2,1],'r')
        self.axes.plot([1,2,3],[1,2,3],'g')
        super(MplCanvas, self).__init__(self.fig)
'''
mpl.use('Qt5Agg')
app = QApplication(sys.argv)
mw = QMainWindow()
widget = QWidget()

layout = QVBoxLayout()

exx = MplCanvas()
layout.addWidget(exx)
widget.setLayout(layout)
mw.setCentralWidget(widget)
mw.show()
sys.exit(app.exec_())'''



from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QObject, pyqtSlot

class ButtonHandler(QObject):
    @pyqtSlot()
    def handleButton(self):
        sender_button = self.sender()
        button_text = sender_button.text()
        print(f"Button clicked: {button_text}")

app = QApplication([])
window = QMainWindow()
wig = QWidget()
wig.setLayout(QVBoxLayout())
window.setCentralWidget(wig)
button_handler = ButtonHandler()

# Create and connect buttons
buttons = []
button_texts = ["Button 1", "Button 2", "Button 3"]  # Example button texts
for text in button_texts:
    button = QPushButton(text)
    button.clicked.connect(button_handler.handleButton)
    buttons.append(button)
    window.centralWidget().layout().addWidget(button)

window.show()
app.exec_()