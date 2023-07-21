class Job:
    
    def __init__(self,data,title):
        self.data=data
        self.title = title
    @classmethod
    def fromLists(cls,keys,values,title):
        data={}
        for index,key in keys:
            data[key]=values[index]
        cls(data,title)
    def __str__(self):
        return self.title