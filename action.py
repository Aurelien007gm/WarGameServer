class Action:

    def  __init__(self,name,**kwargs):
        self.name = name
        self.args = kwargs
        self.value = self.GetValue()

    def GetValue(self):
        dictionnary = {"SetContract":0.5,"Deploy":1,"DiscardCard":0.9,"Transfer":2,"Attack":3}
        get = dictionnary.get(self.name) or 5
        return(get)
    
    def print(self):
        print(self.name)
        print(self.args)

class ActionHandler:
    def __init__(self):
        self.t0 = None
        self.t1 = None
        self.field = 0
        self.navy = 0
        self.para = 0
        self.player = None
        self.name = None

    def Add(self,arg):
        if(arg == "Validate"):
            act = self.BuildAction()
            return(act)
        elif(arg == "Field"):
            self.field += 1
        elif(arg == "Navy"):
            self.navy += 1
        elif(arg == "Para"):
            self.navy += 1
        elif(arg =="Player1"):
            self.player = 0
        elif(arg =="Player2"):
            self.player = 1
        elif(arg =="Player3"):
            self.player = 2
        elif(arg =="Player4"):
            self.player = 3
        elif(isinstance(arg,int)):
            if(not self.t0 is None):
                self.t1 = arg
            else:
                self.t0 = arg
        elif(arg in ["Deploy","DiscardCard","Transfer","Attack"]):
            self.name = arg
        return(None)

    def BuildAction(self):
        act = None
        if(self.name):
            kwargs = {"t0":self.t0,"t1":self.t1,"player":self.player,"field":self.field,"navy":self.navy,"para":self.para}
            act = Action(self.name,**kwargs)
           
        self.t0 = None
        self.t1 = None
        self.player = None
        self.field = 0
        self.navy = 0
        self.para = 0
        self.name = None
        return(act)



    
