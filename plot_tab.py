from PyQt5.QtWidgets import QWidget, QHBoxLayout,QVBoxLayout,QGridLayout,QLabel,QFrame,QListWidget,QListWidgetItem,QPushButton,QLineEdit,QFileDialog,QDialog,QComboBox,QGroupBox
from PyQt5.QtCore import pyqtSlot,QObject
import os
from workspace import Workspace
import vispy.scene
from vispy.scene import visuals
from vispy import app
import vispy.plot as vis

#import matplotlib
#matplotlib.use('Qt5Agg')
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from jobs_tab import clearLayout,clearWidget
from QPlotForm import QPlotForm


class PlotTab(QWidget):
    def __init__(self,statusMessenger,parent):
        super().__init__(parent)
        self.initialized = False
        self.message = statusMessenger

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.

        #plt.rcParams["savefig.directory"] = os.path.dirname(os.curdir)
        
        self.layout = QGridLayout()
        
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.graph_layout = QVBoxLayout()
        self.setup_graph_layout()
        
        self.layout.addLayout(self.graph_layout,0,1,2,1)


        self.formlayout = QVBoxLayout()

        self.graphTypelabel = QLabel("Graph Type")
        self.graph_type_dropdown = QComboBox()
        self.graph_type_dropdown.addItems(QPlotForm.VALID_CONFIGS)
        self.graph_type_dropdown.currentTextChanged.connect(self.redraw_all_forms)
        hhb = QHBoxLayout()
        hhb.addWidget(self.graphTypelabel)
        hhb.addWidget(self.graph_type_dropdown)
        self.formlayout.addLayout(hhb)

        self.graph_forms = []
        self.add_form()

        self.buttons_layout = QHBoxLayout()
        self.plotButton = QPushButton("Plot")
        self.plotButton.clicked.connect(self.update_plot)
        self.buttons_layout.addWidget(self.plotButton,stretch=2)

        self.add_curve_button = QPushButton("+")
        self.buttons_layout.addWidget(self.add_curve_button)
        self.add_curve_button.clicked.connect(self.add_form)

        self.remove_curve_button = QPushButton("-")
        self.buttons_layout.addWidget(self.remove_curve_button)
        self.remove_curve_button.clicked.connect(self.remove_form)

        self.formlayout.addLayout(self.buttons_layout)
        
        
        
        self.layout.addLayout(self.formlayout,0,0)
        self.setLayout(self.layout)
        self.initialized = True
        self.show()

    def setup_graph_layout(self,_3D=False):
        clearLayout(self.graph_layout)
        if not _3D:
            self.fig = vis.Fig()

        #axis = visuals.XYZAxis(parent=self.view.scene)
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.graph_layout.addWidget(self.fig.native)

    
    
    @pyqtSlot()
    def update_plot(self):
        # Drop off the first y element, append a new one.
        #self.sc.axes.cla()  # Clear the canvas.
        scatter = None
        match self.graph_type_dropdown.currentText():
            case "2D":
                self.setup_graph_layout()
                for index,plot in enumerate(self.graph_forms):
                    if  plot.ready and plot.varToPlot != {}:
                        scatter = self.plot2D(plot.vars[plot.varToPlot[0].currentText()],plot.vars[plot.varToPlot[1].currentText()],plot.color.name(),plot.label)
                if(len(self.graph_forms)>1):
                    self.sc.axes.legend()
            case "3D":
                self.setup_graph_layout(True)
                for index,plot in enumerate(self.graph_forms):
                    if  plot.ready and plot.varToPlot != {}:   
                        scatter = self.plot3D(plot.vars[plot.varToPlot[0].currentText()],plot.vars[plot.varToPlot[1].currentText()],plot.vars[plot.varToPlot[2].currentText()])
        # Trigger the canvas to update and redraw.
        self.view.add(scatter)
        self.canvas.update()
    
    

    @pyqtSlot()
    def redraw_all_forms(self):
        for i in range(len(self.graph_forms)):
            self.graph_forms[i].change_config(self.graph_type_dropdown.currentText())
    
    def draw_form(self,index=-1):
        clearLayout(self.graph_forms[index].layout())
        self.varToPlot[index].clear()
        layout = self.graph_forms[index].layout()
        self.dataFilelabel = QLabel("Data File")
        input_file_entry = QLineEdit()
        i= index
        if index ==-1: 
            self.input_file_entries.append(input_file_entry)
            i = len(self.input_file_entries)-1
        else:
            self.input_file_entries[index] = input_file_entry
        self.file_search_button = CustomPushButton("...",i )
        self.file_validate_button = CustomPushButton("V",i)
        hb = QHBoxLayout()
        hb.addWidget(self.dataFilelabel)
        hb.addWidget(self.input_file_entries[index])
        self.input_file_entries[index].setText(self.filePaths[index])
        hb.addWidget(self.file_search_button)
        hb.addWidget(self.file_validate_button)
        self.file_search_button.clicked.connect(self.button_handler.browseFiles)
        self.file_validate_button.clicked.connect(self.button_handler.validateFileName)
        layout.addLayout(hb)
        match self.graph_type_dropdown.currentText():
            case "2D":
                #Draw form for 2D general plot
                if self.vars[index] == {} and self.initialized:
                    self.message("Plot","No data imported, try adding a file")
                elif self.vars[index] != {} and self.initialized:
                    hx = QHBoxLayout()
                    xlabel = QLabel("x var")
                    xComboBox = QComboBox()
                    xComboBox.addItems(self.vars[index].keys())
                    self.varToPlot[index].append(xComboBox)
                    hx.addWidget(xlabel)
                    hx.addWidget(xComboBox)

                    hy = QHBoxLayout()
                    ylabel = QLabel("y var")
                    yComboBox = QComboBox()
                    yComboBox.addItems(self.vars[index].keys())
                    self.varToPlot[index].append(yComboBox)
                    hy.addWidget(ylabel)
                    hy.addWidget(yComboBox)
                    layout.addLayout(hx)
                    layout.addLayout(hy)
            case "3D":
                #Draw form for 3D general plot
                if self.vars == {}:
                    self.message("Plot","No data imported, try adding a file")
                else:
                    hx = QHBoxLayout()
                    xlabel = QLabel("x var")
                    xComboBox = QComboBox()
                    xComboBox.addItems(self.vars[index].keys())
                    self.varToPlot[index].append(xComboBox)
                    hx.addWidget(xlabel)
                    hx.addWidget(xComboBox)

                    hy = QHBoxLayout()
                    ylabel = QLabel("y var")
                    yComboBox = QComboBox()
                    yComboBox.addItems(self.vars[index].keys())
                    self.varToPlot[index].append(yComboBox)
                    hy.addWidget(ylabel)
                    hy.addWidget(yComboBox)

                    hz = QHBoxLayout()
                    zlabel = QLabel("z var")
                    zComboBox = QComboBox()
                    zComboBox.addItems(self.vars[index].keys())
                    self.varToPlot[index].append(zComboBox)
                    hz.addWidget(zlabel)
                    hz.addWidget(zComboBox)

                    #ht = QHBoxLayout()
                    #tlabel = QLabel("time var")
                    #tComboBox = QComboBox()
                    #tComboBox.addItems(self.vars.keys()+['None'])
                    #self.varToPlot.append(tComboBox)
                    #ht.addWidget(tlabel)
                    #ht.addWidget(tComboBox)

                    layout.addLayout(hx)
                    layout.addLayout(hy)
                    layout.addLayout(hz)
                    #layout.addLayout(ht)
                pass
            case "mh loop":
                #Draw form for mH loop in particular
                pass
        self.graph_forms[index].setLayout(layout)
    @pyqtSlot()
    def add_form(self):
        index = len(self.graph_forms)+1
        self.graph_forms.append(QPlotForm("Graph {}".format(index),index,self.message,self.graph_type_dropdown.currentText()))
        self.formlayout.insertWidget(len(self.graph_forms),self.graph_forms[-1])
    @pyqtSlot()
    def remove_form(self):
        form = self.graph_forms.pop()
        clearWidget(form)
        
        self.formlayout.removeWidget(form)
        form.deleteLater()
        
        
        
    def plot2D(self,X,Y,color,label):
        #self.sc.axes.plot(X, Y, color=color,label=label)
        scatter = visuals.Line([[X[i],Y[i]]for i in range(len(X))], color = color)
        return scatter
    def plot3D(self,x,y,z,t=''):
        
        self.sc.axes.set_xlabel('x')
        self.sc.axes.set_ylabel('y')
        self.sc.axes.set_zlabel('z')
        self.sc.axes.plot(x, z,'b', zs=max(y)*2, zdir='y') #curve on y=0
        self.sc.axes.plot(x, y,'b', zs=min(z)*2, zdir='z') #curve on z=0
        self.sc.axes.plot(y, z,'b', zs=min(x)*2, zdir='x') #curve on x=0
        cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["red","orange","green"])
        for i in range(len(x)-1):
            self.sc.axes.plot(x[i:i+2], y[i:i+2], z[i:i+2], color= cmap(i/len(x)))
        
        ax = self.sc.fig.add_axes([.9,0.3,0.1,0.5])
        ax.axis('off')

        self.sc.fig.colorbar(cm.ScalarMappable(mpl.colors.Normalize(), cmap=cmap),ax=ax,location='left')

class Canvas:

    def __init__(self, parent=None, width=5, height=4, dpi=100,_3D=False):
        self.fig = vp.Fig(figsize=(width, height), show=True)
        if(_3D):self.axes = self.fig.add_subplot(projection='3d')
        else: self.axes = self.fig.add_subplot()



