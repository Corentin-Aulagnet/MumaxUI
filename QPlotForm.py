from PyQt5.QtWidgets import QColorDialog,QWidget, QHBoxLayout,QVBoxLayout,QGridLayout,QLabel,QFrame,QListWidget,QListWidgetItem,QPushButton,QLineEdit,QFileDialog,QDialog,QComboBox,QGroupBox
from PyQt5.QtCore import pyqtSlot,QObject,QSize
from PyQt5.QtGui import QPainter,QColor
from typing import Literal,Tuple,get_args
from jobs_tab import clearLayout,clearWidget
import os
from output_file_reader import read_vars
from enum import Enum
class CustomPushButton(QPushButton):

    def __init__(self,text,index):
        super().__init__(text)
        self.index = index

class ButtonHandler(QObject):

    def __init__(self,f1,f2):
        super().__init__()
        self.browserFunction = f1
        self.validateFunction = f2

    @pyqtSlot()
    def browseFiles(self):
        sender_button = self.sender()
        button_index = sender_button.index
        print(f"Button clicked: {button_index}")
        self.browserFunction(button_index)
        return button_index
    
    @pyqtSlot()
    def validateFileName(self):
        sender_button = self.sender()
        button_index = sender_button.index
        print(f"Button clicked: {button_index}")
        self.validateFunction(button_index)
        return button_index
    



class QPlotForm(QGroupBox):

   
    
    _CONFIG = Literal["2D", "3D", "mh loop"]
    VALID_CONFIGS : Tuple[_CONFIG, ...] = get_args(_CONFIG)

    def __init__(self,title,index,statusMessenger,config : _CONFIG = '2D'):
        super().__init__(title)
        self.initialized = False
        self.message = statusMessenger
        self.button_handler = ButtonHandler(self._openFileBrowser,self._validate_read_file)
        self.filePath = ''
        self.vars = {}
        self.varToPlot = []
        self.id = index
        self.setLayout(QVBoxLayout())
        
        self.config = config
        self.input_file_entry = QLineEdit()
        self.labelEntry = QLineEdit()
        self.label=''
        self.color =QColor(0,0,255)
        self.draw_form()
        self.initialized = True
        self.ready = False

    def draw_form(self):
        clearLayout(self.layout())
        self.varToPlot.clear()
        layout = self.layout()
        self.dataFilelabel = QLabel("Data File")
        self.input_file_entry = QLineEdit()
        self.file_search_button = CustomPushButton("...",self.id )
        self.file_validate_button = CustomPushButton("V",self.id)
        hb = QHBoxLayout()
        hb.addWidget(self.dataFilelabel)
        hb.addWidget(self.input_file_entry)
        self.input_file_entry.setText(self.filePath)
        hb.addWidget(self.file_search_button)
        hb.addWidget(self.file_validate_button)
        self.file_search_button.clicked.connect(self.button_handler.browseFiles)
        self.file_validate_button.clicked.connect(self.button_handler.validateFileName)
        layout.addLayout(hb)
        match self.config:
            case "2D":
                #Draw form for 2D general plot
                if self.vars == {} and self.initialized:
                    self.message("Plot","No data imported, try adding a file")
                    self.input_file_entry.setText('')

                elif self.vars != {} and self.initialized:
                    hx = QHBoxLayout()
                    xlabel = QLabel("x var")
                    xComboBox = QComboBox()
                    xComboBox.addItems(self.vars.keys())
                    self.varToPlot.append(xComboBox)
                    hx.addWidget(xlabel)
                    hx.addWidget(xComboBox)

                    hy = QHBoxLayout()
                    ylabel = QLabel("y var")
                    yComboBox = QComboBox()
                    yComboBox.addItems(self.vars.keys())
                    self.varToPlot.append(yComboBox)
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
                    xComboBox.addItems(self.vars.keys())
                    self.varToPlot.append(xComboBox)
                    hx.addWidget(xlabel)
                    hx.addWidget(xComboBox)

                    hy = QHBoxLayout()
                    ylabel = QLabel("y var")
                    yComboBox = QComboBox()
                    yComboBox.addItems(self.vars.keys())
                    self.varToPlot.append(yComboBox)
                    hy.addWidget(ylabel)
                    hy.addWidget(yComboBox)

                    hz = QHBoxLayout()
                    zlabel = QLabel("z var")
                    zComboBox = QComboBox()
                    zComboBox.addItems(self.vars.keys())
                    self.varToPlot.append(zComboBox)
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

        self.labelLayout = QHBoxLayout()
        self.labelLayout.addWidget(QLabel("Legend label"))
        self.labelEntry = QLineEdit()
        self.labelEntry.setText(self.label)
        self.labelEntry.textChanged.connect(self.updateLabel)
        self.labelLayout.addWidget(self.labelEntry)
        layout.addLayout(self.labelLayout)


        self.colorLayout = QHBoxLayout()
        self.colorLayout.addWidget(QLabel("Color"))
        colorButton = ClickableSquare(self,QColor(self.color))
        self.colorLayout.addWidget(colorButton)
        layout.addLayout(self.colorLayout)
        self.setLayout(layout)
    @pyqtSlot(str)
    def updateLabel(self,text):
        self.label = text
    def _openFileBrowser(self,index):
        self.filePath =  QFileDialog.getOpenFileName (None,'Data File',os.getcwd())[0]
        self.input_file_entry.setText(self.filePath)
        self._validate_read_file(index)

    def _validate_read_file(self,index):
        self.vars.clear()
        self.filePath = self.input_file_entry.text()
        if(not os.path.isfile(self.filePath)):
            self.ready = False
            self.input_file_entry.setText(self.filePath)
            self.message("Plots","No data file found, try adding a valid file")
        elif (self.filePath == ""):
            self.ready = False
            self.input_file_entry.setText(self.filePath)
            self.message("Plots","No data file, try adding a file")
        else:
            self.input_file_entry.setText(self.filePath)
            self.vars = read_vars(self.filePath)
            self.draw_form()
            self.ready = True
            self.message("Plots","Data file loaded")

    def change_config(self,config):
        self.config = config
        self.draw_form()


class ClickableSquare(QWidget):
    def __init__(self,plot : QPlotForm,color=QColor(0,0,255)):
        super().__init__()
        self.initUI()
        self.color= color
        self.plot = plot

    def initUI(self):
        self.setGeometry(0, 0, 20, 20)

    def mousePressEvent(self, event):
        prev = self.color
        self.color = QColorDialog.getColor()
        if(self.color.name() == '0xffffff'):
            self.color = prev
        self.plot.color = self.color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the square dimensions
        square_size = int(min(self.width(), self.height()))
        square_x = int((self.width() - square_size) / 2)
        square_y = int((self.height() - square_size) / 2)
        # Fill the square with a color
        painter.fillRect(square_x, square_y, square_size, square_size, self.color)

    def sizeHint(self):
        return QSize(20, 20)