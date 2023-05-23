from PyQt5.QtWidgets import QDialog,QVBoxLayout,QHBoxLayout,QListWidget,QListWidgetItem,QLabel,QPushButton,QLineEdit
from PyQt5.QtCore import pyqtSlot
from workspace import Workspace
class AddKeyPopup(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        #Layouts
        self.display_layout = QVBoxLayout(self)
        self.add_layout = QHBoxLayout(self)
        ##Keys Display
        self.list = QListWidget(self)
        for index,key in enumerate(Workspace.keys):
            self.list.addItem(key)
        
        self.list.itemDoubleClicked.connect(self._remove)
        self.display_layout.addWidget(self.list)
        ##Add key form
        
        self.label = QLabel("Key Name")
        self.key_name_edit = QLineEdit(self)
        self.add_button = QPushButton("+",self)
        self.add_button.clicked.connect(self._addKey)
        self.add_layout.addWidget(self.label)
        self.add_layout.addWidget(self.key_name_edit)
        self.add_layout.addWidget(self.add_button)

        self.display_layout.addLayout(self.add_layout)
        self.setLayout(self.display_layout)


        self.show()
    @pyqtSlot()
    def _addKey(self):
        text = self.key_name_edit.text()
        item = QListWidgetItem(text)
        Workspace.addKey(text)
        self.list.addItem(text)
    @pyqtSlot(QListWidgetItem)
    def _remove(self,item):
        item_text = item.text()
        Workspace.removeKey(item_text)
        self.list.clear()
        self.list.addItems(Workspace.keys)