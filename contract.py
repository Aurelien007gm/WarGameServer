class Contract:

    def __init__(self):
        self.isFailed = False
        self.isSuccess = False
        self.description = "Basic contract"
        self.name = "Basic contract"
        self.countdown = 4
        self.player = None
        self.reward = 1000
        self.gage = -500
    
    def SetPlayer(self,p):
        self.player = p

    def Print(self):
        print(f"Contract {self.name} is possed by {self.player.name}")



    def EndTurn(self):
        self.countdown -= 1
        if(self.countdown <=0):
            if(self.isSuccess and not self.isFailed):
                self.player.AddMoney(self.reward)
                print(f"Contract {self.name} was done by {self.player.name} !")
            else:
                self.player.AddMoney(self.gage)
                print(f"Contract {self.name} was failed by {self.player.name} !")
    
    def CheckDelete(self):
        # return if the contract should be deleted or not
        return(self.countdown <= 0)
    
    def Fail(self,arg):
        return
    
class Stingy(Contract):
    def __init__(self):
        super().__init__()
        self.reward = 5000
        self.isSuccess = True
        self.name = "Stingy"
        self.description = "Do not spend money in next 4 turns"

    def Fail(self,arg):
       if(arg == "MoneySpend"):
           self.isSuccess = False
           self.isFailed = False




    