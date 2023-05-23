from PyQt5.QtWidgets import QWidget, QVBoxLayout,QLabel
from QTextEditHighlighter import QTextEditHighlighter
from PyQt5.QtCore import pyqtSlot
from workspace import Workspace
from QTextEditHighlighter import MumaxGoHighlighter
class TemplateEditTab(QWidget):
    text=''
    def __init__(self,statusMessenger,parent):
        super(QWidget,self).__init__(parent)
        self.message = statusMessenger
        self.layout = QVBoxLayout(self)
        self._current_filename = "temp.mx3"

        #Text Edit to edit the template file
        self._editer = QTextEditHighlighter()
        self.highlighter = MumaxGoHighlighter(self._editer.document())
        #Label to display current file edited
        self._hasUnsavedChanges = False
        self._current_label = QLabel(self._current_filename)

        self._editer.textChanged.connect(self._fileEdited)


        self.layout.addWidget(self._current_label)
        self.layout.addWidget(self._editer)

        self.setLayout(self.layout)

    def setFilename(self,new_file_name):
        self._current_filename = new_file_name
        self._current_label.setText(self._current_filename)

    def openFile(self, file_name):
        f = open(file_name,'r')
        text = f.readlines()
        text = ''.join(text)
        self._editer.setText(text)
        self._hasUnsavedChanges = False
        Workspace.setTemplateFile(file_name)
        self.setFilename(file_name)
        f.close()

    def saveFile(self,file_name):
        text = self._editer.toPlainText()
        self.setFilename(file_name)
        self._hasUnsavedChanges = False
        return text

    @pyqtSlot()
    def _fileEdited(self):
        if(not self._hasUnsavedChanges):
            TemplateEditTab.text = self._editer.toPlainText()
            self._hasUnsavedChanges = True
            self._current_label.setText(self._current_filename+'*')

