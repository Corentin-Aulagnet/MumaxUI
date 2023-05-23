import os
import xml.etree.ElementTree as ET
from job import Job
class Workspace:
    jobs =[]
    keys= set({})
    template_file = ''
    jobs_file = ''
    outputDir =''
    path = ''
    def __init__(self):
        pass
    @staticmethod
    def addKey(key):
        Workspace.keys.add(key)
        for job in Workspace.jobs:
            if not key in job.data.keys():
                job.data[key] = ''

    @staticmethod
    def removeKey(key):
        if(key in Workspace.keys):
             Workspace.keys.remove(key)

    @staticmethod
    def setTemplateFile(filename):
        Workspace.template_file = filename
    
    @staticmethod
    def setOutputDir(path):
        Workspace.outputDir = path
    @staticmethod
    def getOutputDir():
        return Workspace.outputDir

    @staticmethod
    def saveWorkspace():
        data = ET.Element("MumaxMultiThreadInputFile")
        templateElement = ET.SubElement(data,"TemplateFile")
        templateElement.set("path",Workspace.template_file)
        jobsElement = ET.SubElement(data,"jobs")
        tagsElement = ET.SubElement(jobsElement,"tags")
        for tag in Workspace.keys:
            tagElement = ET.SubElement(tagsElement,"tag")
            tagElement.text = tag
        for job in Workspace.jobs:
            jobElement = ET.SubElement(jobsElement,"job")
            jobElement.set("name",job.title)
            for tag in Workspace.keys:
                valueElement = ET.SubElement(jobElement,"value") 
                valueElement.text = job.data[tag]
                valueElement.set('tag',tag)
        s = ET.tostring(data,encoding="unicode")
        f = open(Workspace.jobs_file,'w')
        f.write(s)
        f.close()

    @staticmethod
    def saveWorkspaceAs(filename):
        Workspace.jobs_file = filename
        Workspace.saveWorkspace()
    
