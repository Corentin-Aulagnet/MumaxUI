from PyQt5.QtCore import QRunnable,QObject,pyqtSlot, pyqtSignal
import os
from string import Template
from datetime import datetime
import traceback, sys


def setup_scripts(jobs : list,template_file : str,file_names:list,destination_dir:str = '.\\'):
    #jobs is a list of dict [{val1 : val1, val2: val2},{val1 : val11, val 2:val22}]

    # read template script
    with open(template_file,'r') as f:
        scripttmpl = Template(f.read())

    

    # create a directory for the scripts
    if(not os.path.exists(destination_dir)):
        os.mkdir(destination_dir)

    for index,job in enumerate(jobs):
        # write the script for each theta value
        script = scripttmpl.substitute(job)

        with open(destination_dir+'/'+file_names[index]+'.mx3','w') as f:
            f.write(script)

class PostWorker(QRunnable):
    def __init__(self, fileName,directory):
        super(PostWorker, self).__init__()
        self.fileName = fileName
        self.directory = directory
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        mumaxPath = 'C:\\Go\\bin\\mumax3.10\\mumax3.exe'

        self.signals.started.emit("Starting task {0}".format(self.directory+'/'+self.fileName+'.mx3'))
        os.system("{1} -s {0} > {2}".format(self.directory+'/'+self.fileName+'.mx3',mumaxPath,self.directory+'/'+self.fileName+'.log'))
        self.signals.finished.emit("Finished task {0}".format(self.directory+'/'+self.fileName+'.mx3'))
        

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    started = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)