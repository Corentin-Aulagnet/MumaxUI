from PyQt5.QtWidgets import QLayout,QWidget, QHBoxLayout,QVBoxLayout,QGridLayout,QLabel,QFrame,QListWidget,QListWidgetItem,QPushButton,QLineEdit,QFileDialog,QDialog,QProgressBar
from PyQt5.QtCore import pyqtSlot,QThreadPool,Qt
from job import Job
import os
from workspace import Workspace
import xml.dom.minidom as minidom


from multi_threader import PostWorker,setup_scripts
def clearLayout(layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    clearLayout(child)

def clearWidget(widget):
    children = widget.findChildren(QWidget)
    for child in children:
        child.deleteLater()
    children = widget.findChildren(QLayout)
    for child in children:        
        clearLayout(child)
class JobListItem(QListWidgetItem):

    def __init__(self,job:Job,parent):
        super().__init__(str(job),parent,1000)
        self.job = job


class JobEditTab(QWidget):
    def __init__(self,statusMessenger,parent):
        super(QWidget,self).__init__(parent)
        self.message = statusMessenger
        self.main_layout = QHBoxLayout(self)
        
        self.threadpool = QThreadPool()
        self.current_progress = 0
        self._current_filename = "temp.xml"

        #Job file part
        self._list_widget = QListWidget(self)
        self._list_widget.itemDoubleClicked.connect(self._modify_job)
        
        ##Layout
        self.job_file_layout = QVBoxLayout(self)
        self.job_file_layout.addWidget(self._list_widget)
        
        #self.job_file_layout.addWidget(self._editer)

        #Job Creation part
        #Layout
        self.job_creation_layout = QVBoxLayout(self)
        ##JobCreation Form
        self.key_input_dict = {}
        self.jobs_form_layout = QGridLayout(self)
        self.redrawForm()
        ##Separator
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine | QFrame.Plain)
        self.line.setFrameShadow(QFrame.Sunken)
        ##Launch setup
        ###Pools
        self.pool_layout = QHBoxLayout(self)
        self.pool_label = QLabel("Max number of thread to allocate")
        self.pool_entry = QLineEdit(self)
        self.pool_layout.addWidget(self.pool_label)
        self.pool_layout.addWidget(self.pool_entry)
        ###OutputDir
        self.outDir_layout = QHBoxLayout(self)
        self.outputDirLabel = QLabel("Output Directory",self)
        self.directory_entry = QLineEdit(self)
        self.directory_entry.textChanged.connect(self._updateOutputDir)
        self.directory_browser_button = QPushButton('...',self)
        self.directory_browser_button.clicked.connect(self._openDirectoryBrowser)
        self.outDir_layout.addWidget(self.outputDirLabel)
        self.outDir_layout.addWidget(self.directory_entry)
        self.outDir_layout.addWidget(self.directory_browser_button)
        ###Fire&Setup
        self.fire_layout = QVBoxLayout(self)
        self.fire_buttons_layout = QHBoxLayout(self)
        self._launch_button = QPushButton('Launch',self)
        self._launch_button.clicked.connect(self._launch)
        self._setup_button = QPushButton('Setup Files',self)
        self._setup_button.clicked.connect(self._setup)
        self._progressBar = QProgressBar(self)
        self._progressBar.setMinimum(0)

        self.fire_buttons_layout.addWidget(self._setup_button)
        self.fire_buttons_layout.addWidget(self._launch_button)
        self.fire_layout.addLayout(self.fire_buttons_layout)
        self.fire_layout.addWidget(self._progressBar)

        ##Layout
        self.jobs_launch_layout = QVBoxLayout(self)
        self.jobs_launch_layout.addWidget(self.line)
        self.jobs_launch_layout.addLayout(self.pool_layout)
        self.jobs_launch_layout.addLayout(self.outDir_layout)
        self.jobs_launch_layout.addLayout(self.fire_layout)

        self.job_creation_layout.addLayout(self.jobs_form_layout)
        self.job_creation_layout.addLayout(self.jobs_launch_layout)

        self.main_layout.addLayout(self.job_file_layout)
        self.main_layout.addLayout(self.job_creation_layout)
        self.setLayout(self.main_layout)
    
    def redrawForm(self):
        self.key_input_dict.clear()
        clearLayout(self.jobs_form_layout)


        
        label = QLabel("Title")
        self.jobs_form_layout.addWidget(label,0,0)
        entry = QLineEdit(self)
        self.key_input_dict = {}
        self.key_input_dict["Title"] = entry
        self.jobs_form_layout.addWidget(entry,0,1)

        for index,key in enumerate(Workspace.keys):
            label = QLabel(key)
            self.jobs_form_layout.addWidget(label,index+1,0)
            entry = QLineEdit(self)
            self.key_input_dict[key] = entry
            self.jobs_form_layout.addWidget(entry,index+1,1)
        
        self.update_button = QPushButton("Add")
        self.update_button.clicked.connect(self._add_job_from_form)
        self.jobs_form_layout.addWidget(self.update_button,len(Workspace.keys)+1,0)       
    
    @pyqtSlot()
    def _add_job_from_form(self):
        new_job = self._readJobForm()
        Workspace.jobs.append(new_job)
        self._populate_job(new_job)

    def _add_job(self,job):
        Workspace.jobs.append(job)
        self._populate_job(job)

    def repopulate_jobs(self):
        self._list_widget.clear()
        for job in Workspace.jobs:
            self._populate_job(job)

    def _populate_job(self,job):
        new_job_item = JobListItem(job,self._list_widget)
        new_job_item.setFlags(new_job_item.flags() or Qt.ItemIsUserCheckable)
        new_job_item.setCheckState(Qt.Unchecked)
        self._list_widget.addItem(new_job_item)

    @pyqtSlot(QListWidgetItem)
    def _remove_job(self,item):
        job = item.job
        Workspace.jobs.remove(job)
        self._list_widget.clear()
        for job in Workspace.jobs:
            job_item = JobListItem(job,self._list_widget)
            self._list_widget.addItem(job_item)

    @pyqtSlot(QListWidgetItem)
    def _modify_job(self,item):
        popup = ModifyJobPopup(item.job,self)
        popup.exec()
        self.repopulate_jobs()

    @pyqtSlot()
    def _openDirectoryBrowser(self):
        directoryPath =  QFileDialog.getExistingDirectory (None,'Output Directory',os.getcwd())
        self.directory_entry.setText(directoryPath)

    @pyqtSlot()
    def _updateOutputDir(self):
        if(self.directory_entry.text()==''):Workspace.setOutputDir('./')
        else : Workspace.setOutputDir(self.directory_entry.text())
    @pyqtSlot()
    def _setup(self):

        template_file = Workspace.template_file
        checked_jobs = self.find_checked_jobs()
        try:
            setup_scripts([checked_jobs[i].data for i in range(len(checked_jobs))] ,template_file,[checked_jobs[i].title for i in range(len(checked_jobs))],Workspace.outputDir)
            self.message("Jobs","Files successfully set up")
        except FileNotFoundError:
            self.message("Jobs","Verify the output path")
    @pyqtSlot()
    def _launch(self):
        checked_jobs = self.find_checked_jobs()
        try:
            pool_size = int(self.pool_entry.text())
            self.threadpool.setMaxThreadCount(pool_size)
            workers = []
            self.current_progress = 0
            self._progressBar.setMaximum(len(checked_jobs))
            self._progressBar.setValue(0)
            for i in range(len(checked_jobs)):
                worker = PostWorker(checked_jobs[i].title,Workspace.outputDir)
                workers.append(worker)
                worker.signals.finished.connect(self.update_progress_bar)
                worker.signals.started.connect(self.job_started)
                self.threadpool.start(worker)
            
            self.message("Jobs","Computation started from {}".format(Workspace.path))
        except ValueError:
            self.message("Jobs", "ValueError, check the number of thread to allocate")
        
    @pyqtSlot(str)
    def job_started(self,filename):
        self.message("Jobs",filename)
    @pyqtSlot(str)
    def update_progress_bar(self,filename):
        self.current_progress +=1
        self._progressBar.setValue(self.current_progress)
        self.message("Jobs",filename)
    def find_checked_jobs(self):
        checked = []
        for index in range(self._list_widget.count()):
            job_item = self._list_widget.item(index)
            if job_item.checkState():
                checked.append(Workspace.jobs[index])
        return checked
    def _readJobForm(self):
        data={}
        title=''
        for key,entryField in self.key_input_dict.items():
            if key == 'Title': title = entryField.text()
            else: data[key] = entryField.text()
        job = Job(data,title)
        return job
            

    def setFilename(self,new_file_name):
        self._current_filename = new_file_name
        self._current_label.setText(self._current_filename)

    def openFile(self, file_name):
        jobsToAdd,keysToAdd = self.parse_job_file(file_name)
        self._list_widget.clear()
        for job in jobsToAdd:
            self._add_job(job)
        for key in keysToAdd:
            Workspace.addKey(key)
        self.redrawForm()
        

    def saveFile(self,file_name):
        text = self._editer.toPlainText()
        self.setFilename(file_name)
        self._hasUnsavedChanges = False
        return text

    def parse_job_file(self,path):
        #parse input file
        dom = minidom.parse(path)
        root = dom.documentElement
        Workspace.template_file = dom.getElementsByTagName("TemplateFile").item(0).getAttribute('path')
        tags = dom.getElementsByTagName("tag")
        tagList =[]
        for tag in tags:
            tagList.append(tag.firstChild.nodeValue)
        jobs = dom.getElementsByTagName('job')
        jobList = []
        for job in jobs:
            jobDict={}
            title = job.getAttribute('name')
            values = job.getElementsByTagName('value')
            for index,value in enumerate(values):
                jobDict[value.getAttribute('tag')]= value.firstChild.nodeValue

            jobList.append(Job(jobDict,title))
        return jobList,tagList
    
    @pyqtSlot()
    def _fileEdited(self):
        if(not self._hasUnsavedChanges):
            self._hasUnsavedChanges = True
            self._current_label.setText(self._current_filename+'*')


class ModifyJobPopup(QDialog):
    def __init__(self,job : Job,parent):
        super().__init__(parent)
        self._parent = parent
        self.old_job = job
        self.jobs_form_layout = QGridLayout(self)
        
        label = QLabel("Title")
        self.jobs_form_layout.addWidget(label,0,0)
        entry = QLineEdit(self)
        entry.setText(job.title)
        self.key_input_dict = {}
        self.key_input_dict["Title"] = entry
        self.jobs_form_layout.addWidget(entry,0,1)

        index=0
        for index,key in enumerate(Workspace.keys):
            label = QLabel(key)
            self.jobs_form_layout.addWidget(label,index+1,0)
            entry = QLineEdit(self)
            entry.setText(job.data[key])
            self.key_input_dict[key] = entry
            self.jobs_form_layout.addWidget(entry,index+1,1)
        
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.updateJob)
        self.jobs_form_layout.addWidget(self.update_button,index+2,0)
        self.remove_button = QPushButton("Remove")
        self.remove_button.setStyleSheet('QPushButton {color: red;}')
        self.remove_button.clicked.connect(self.removeJob)
        self.jobs_form_layout.addWidget(self.remove_button,index+2,1)

    @pyqtSlot()
    def updateJob(self):
        index = Workspace.jobs.index(self.old_job)
        Workspace.jobs.remove(self.old_job)
        data={}
        title=''
        for key,entryField in self.key_input_dict.items():
            if key == 'Title': title = entryField.text()
            else: data[key] = entryField.text()
        job = Job(data,title)
        Workspace.jobs.insert(index,job)
        self.close()

    @pyqtSlot()
    def removeJob(self):
        index = Workspace.jobs.index(self.old_job)
        Workspace.jobs.remove(self.old_job)
        self.close()
        
