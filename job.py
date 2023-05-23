class Job:
    def __init__(self,keys,values,title):
        self.data={}
        for index,key in keys:
            self.data[key]=values[index]
        self.title = title
    def __init__(self,data,title):
        self.data=data
        self.title = title
    def __str__(self):
        return self.title