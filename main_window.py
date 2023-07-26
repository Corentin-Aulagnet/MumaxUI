from PyQt5.QtWidgets import QDockWidget,QMainWindow, QWidget, QAction, QTabWidget,QVBoxLayout, QFileDialog,QStatusBar,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,Qt
from datetime import datetime
import os
from template_tab import TemplateEditTab
from add_key_popup import AddKeyPopup
from jobs_tab import JobEditTab
from plot_tab import PlotTab
from workspace import Workspace
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #Defining the main window
        self.title= "Mumax MultiThreader Environment"
        self.left = 300
        self.top = 300
        self.width = 1400
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        

        
        #Central Widget
        #self.table_widget = MyTableWidget(self)
        self.setCentralWidget(QWidget())
        self.centralWidget().hide()

        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.ForceTabbedDocks | QMainWindow.AllowNestedDocks)
        #create logview
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.logDock = QDockWidget("Logs")
        self.logDock.setWidget(self.log)
        self.addDockWidget(Qt.BottomDockWidgetArea,self.logDock)

        self.template_tab = TemplateEditTab(self.logInfo,self)
        self.templateDock = QDockWidget("Template")
        self.templateDock.setWidget(self.template_tab)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.templateDock)

        self.jobs_tab = JobEditTab(self.logInfo,self)
        self.jobsDock = QDockWidget("Jobs")
        self.jobsDock.setWidget(self.jobs_tab)
        self.tabifyDockWidget(self.templateDock,self.jobsDock)

        self.plot_tab = PlotTab(self.logInfo,self)
        self.plotDock = QDockWidget("Plot")
        self.plotDock.setWidget(self.plot_tab)
        self.addDockWidget(Qt.RightDockWidgetArea,self.plotDock)

        #Creating Menus
        self._createMenus()

        self.show()


    def logInfo(self,sender,message):
        self.log.append(str(datetime.now())+' ' + sender + ': '+message+'\n')

    def _createMenus(self):
        #Menu bar
        self.menu_bar = self.menuBar()
        ##Workspace Menu
        self.workspace_menu = self.menu_bar.addMenu("&Workspace")
        ##Open Workspace Action
        self.open_workspace_action = QAction("Open Workspace...",self)
        self.open_workspace_action.setShortcut('Ctrl+O')
        ##Save Workspace Action
        self.save_workspace_action = QAction("Save Workspace",self)
        self.save_workspace_action.setShortcut('Ctrl+S')
        self.save_workspace_action.triggered.connect(self._saveWorkspace)
        self.workspace_menu.addAction(self.save_workspace_action)
        ###Save Workspace As action
        self.save_workspace_as_action = QAction("Save Workspace As...",self)
        self.save_workspace_as_action.setShortcut('Ctrl+Shift+S')
        self.workspace_menu.addAction(self.save_workspace_as_action)
        self.save_workspace_as_action.triggered.connect(self._saveWorkspaceAs)
         ###Open Workspace action
        self.open_workspace_action = QAction("Open Workspace...",self)
        self.open_workspace_action.setShortcut('Ctrl+O')
        self.workspace_menu.addAction(self.open_workspace_action)
        self.open_workspace_action.triggered.connect(self._openWorkspace)
        ##Template Menu
        self.template_menu = self.menu_bar.addMenu("&Template")
        ###Save Template As action
        self.save_template_as_action = QAction("Save Template As...",self)
        self.template_menu.addAction(self.save_template_as_action)
        self.save_template_as_action.triggered.connect(self._saveTemplateAs)
        ###Save Template action
        self.save_template_action = QAction("Save Template",self)
        self.template_menu.addAction(self.save_template_action)
        self.save_template_action.triggered.connect(self._saveTemplate)
        ###Open Template action
        self.open_template_action = QAction("Open Template...",self)
        self.template_menu.addAction(self.open_template_action)
        self.open_template_action.triggered.connect(self._openTemplate)
        ##Jobs Menu
        self.jobs_menu = self.menu_bar.addMenu("&Jobs")
        ###Modify keys action
        self.modify_keys_action = QAction("Modify keys",self)
        self.modify_keys_action.setShortcut('Ctrl+K');
        self.jobs_menu.addAction(self.modify_keys_action)
        self.modify_keys_action.triggered.connect(self._modifyKeys)
        ###Load job file
        self.open_jobs_action = QAction("Open Jobs File...",self)
        self.jobs_menu.addAction(self.open_jobs_action)
        self.open_jobs_action.triggered.connect(self._openJobs)
        ###Luanch solo job
        self.launch_single_action = QAction("Launch single...",self)
        self.jobs_menu.addAction(self.launch_single_action)
        self.launch_single_action.triggered.connect(self._launchSingle)
        ##Window Menu
        self.window_menu = self.menu_bar.addMenu("&Windows")
        ###Template
        self.template_dock_action = QAction("Template",self)
        self.window_menu.addAction(self.templateDock.toggleViewAction())

        ###jobs
        self.jobs_dock_action = QAction("Jobs",self)
        self.window_menu.addAction(self.jobsDock.toggleViewAction())

        ###plots
        self.plot_dock_action = QAction("Graphs",self)
        self.window_menu.addAction(self.plotDock.toggleViewAction())

        ###logs
        self.logs_dock_action = QAction("Logs",self)
        self.window_menu.addAction(self.logDock.toggleViewAction())


    @pyqtSlot()
    def _modifyKeys(self):
        dialog = AddKeyPopup(self)
        dialog.exec()
        self.jobs_tab.redrawForm()

    @pyqtSlot()
    def _saveWorkspace(self):
        if(Workspace.jobs_file==''): 
            self._saveWorkspaceAs()
        else:
            self._saveTemplate()
            Workspace.saveWorkspace()
    @pyqtSlot()
    def _saveWorkspaceAs(self):
        self._saveTemplateAs()
        save_name = QFileDialog.getSaveFileName(None, 'Save Workspace',os.getcwd(),"Worspace (*.xml)")[0]
        Workspace.saveWorkspaceAs(save_name)
    @pyqtSlot()
    def _openWorkspace(self):
        self._openJobs()
        self._openTemplate(Workspace.template_file)
        os.chdir(Workspace.path)
    @pyqtSlot()
    def _saveTemplateAs(self):
        save_name = QFileDialog.getSaveFileName(None, 'Save Template file',os.getcwd(),"Mumax3 Files (*.mx3 *.txt)")[0]
        if(save_name != ''):
            text = self.template_tab.saveFile(save_name)
            f = open(save_name,'w')
            f.writelines(text)
            f.close()
        else:
            #TODO display something in the status bar
            pass

    @pyqtSlot()
    def _saveTemplate(self):
        save_name = self.template_tab._current_filename
        text = self.template_tab.saveFile(save_name)
        f = open(save_name,'w')
        f.writelines(text)
        f.close()

    @pyqtSlot()
    def _openTemplate(self,file_name=''):
        if(file_name==''):file_name = QFileDialog.getOpenFileName(None, 'Open file', os.getcwd(),"Template files (*.mx3)")[0]
        if(file_name!=''):self.template_tab.openFile(file_name)

    @pyqtSlot()
    def _openJobs(self):
        file_name = QFileDialog.getOpenFileName(None, 'Open file', os.getcwd(),"Jobs Files (*.xml)")[0]
        Workspace.jobs_file = file_name
        Workspace.path = '/'.join(file_name.split('/')[:-1])
        Workspace.jobs = []
        Workspace.keys = set({})
        if(file_name != ''):self.jobs_tab.openFile(file_name)

    @pyqtSlot()
    def _launchSingle(self):
        file_name = QFileDialog.getOpenFileName(None, 'Open file', os.getcwd(),"Mumax3 scripts (*.mx3)")[0]
        job_name = file_name.split('/')[-1][:-4]
        dir_name = '/'.join(file_name.split('/')[:-1])
        os.chdir(dir_name)
        self.jobs_tab.launch_single(job_name,dir_name)
        
class MyTableWidget(QWidget):
    
    def __init__(self,parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.template_tab = TemplateEditTab(self.logInfo,self)
        self.jobs_tab = JobEditTab(self.logInfo,self)
        self.plot_tab = PlotTab(self.logInfo,self)
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.template_tab,"Template")
        self.tabs.addTab(self.jobs_tab,"Jobs")
        self.tabs.addTab(self.plot_tab,"Plot")
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        
        
        self.setLayout(self.layout)
    def logInfo(self,sender,message):
        self.log.append(str(datetime.now())+' ' + sender + ': '+message+'\n')