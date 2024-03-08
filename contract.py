import random as rd
class Contract:

    def __init__(self, **kwargs):
        self.isFailed = False
        self.isSuccess = False
        self.description = "Basic contract"
        self.name = "Basic contract"
        self.countdown = 4
        self.difficulty = "Easy"
        self.player = kwargs.get("player") or None
        self.reward = 2000
        self.gage = -200
        self.tm = kwargs.get("tm")
        self.cm = kwargs.get("cm")
        self.expiration = self.cm.turn + self.countdown
        self.log = kwargs.get("log")
    
    def SetPlayer(self,p):
        self.player = p

    def Print(self):
        print(f"Contract {self.name} is possed by {self.player.name}")

    def SetTm(self,tm):
        self.tm = tm



    def EndTurn(self):
        self.countdown -= 1
        self.log.Info(f"Contract {self.name} own by {self.player.name} will end in {self.countdown} !")
        if(self.countdown <=0):
            if(self.isSuccess and not self.isFailed):
                self.player.AddMoney(self.reward)
                print(f"Contract {self.name} was done by {self.player.name} !")
                self.log.Info(f"Contract {self.name} was done by {self.player.name} !")
            else:
                self.player.AddMoney(self.gage)
                print(f"Contract {self.name} was failed by {self.player.name} !")
                self.log.Info(f"Contract {self.name} was failed by {self.player.name} !")

        ##elif(self.isFailed):
            ##self.player.AddMoney(self.gage)
            ##self.log.Info(f"Contract {self.name} was failed by {self.player.name} !")
    
    def CheckDelete(self):
        # return if the contract should be deleted or not
        return(self.countdown <= 0)
    
    def Fail(self,arg):
        return
    
    def ToJson(self):
        return({"countdown":self.countdown,"description":self.description,"owner":self.player.name,"owner_id":self.player.id,"name":self.name})
    
    def UpdateOnDeploy(self,**kwargs):
        #kwargs are {troop,navy,para}
        return
    
class Stingy(Contract):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.reward = 5000
        self.isSuccess = True
        self.difficulty = "Easy"
        self.name = "Stingy"
        self.description = "Do not spend money in next 4 turns"

    def Fail(self,arg):
       if(arg == "MoneySpend"):
           self.isSuccess = False
           self.isFailed = False

class Hold(Contract):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.reward = 2000
        self.gage = -200
        self.isSuccess = True
        self.name = "Hold"
        self.difficulty = "Easy"
        N = 46
        self.territory_id = kwargs.get("arg") or rd.randint(0,N) 
        self.territory = self.tm.territories[self.territory_id]
        self.description = f"Hold territory {self.territory.name} at the end of turn {self.expiration}"

    def IsSucess(self):
        return(self.territory.owner_id == self.player.id)
    
    def EndTurn(self):
        self.isSuccess = self.IsSucess()
        super().EndTurn()


class Sailor(Contract):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.reward = 2000
        self.gage = -200
        self.isSuccess = True
        self.name = "Sailor"
        self.difficulty = "Easy"
        self.description = f"Deploy at least 5 navy troop before turn {self.expiration}"
        self.deployed = 0
        self.target = 5

    def IsSucess(self):
        return(self.deployed >= self.target)
    
    def UpdateOnDeploy(self,**kwargs):
        navy = kwargs.get("navy") or 0
        self.deployed += navy
    
    def EndTurn(self):
        self.isSuccess = self.IsSucess()
        super().EndTurn()

class Aviator(Contract):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.reward = 5000
        self.gage = -1500
        self.isSuccess = True
        self.name = "Aviator"
        self.difficulty= "Medium"
        self.description = f"Deploy at least 8 navy troop before turn {self.expiration}"
        self.deployed = 0
        self.target = 8

    def IsSucess(self):
        return(self.deployed >= self.target)
    
    def UpdateOnDeploy(self,**kwargs):
        para = kwargs.get("para") or 0
        self.deployed += para
    
    def EndTurn(self):
        self.isSuccess = self.IsSucess()
        super().EndTurn()

class MasterSeaAir(Contract):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.reward = 5000
        self.gage = -1500
        self.isSuccess = True
        self.name = "Master of Sea and Air"
        self.difficulty = "Hard"
        self.description = f"Deploy at least 10 navy troop  and 10 para troop before end of turn {self.expiration}"
        self.navy_deployed = 0
        self.navy_target = 10
        self.para_deployed = 0
        self.para_target = 10

    def IsSucess(self):
        return(self.navy_deployed >= self.navy_target and self.para_deployed >= self.para_target)
    
    def UpdateOnDeploy(self,**kwargs):
        navy = kwargs.get("navy") or 0
        self.navy_deployed += navy
        para = kwargs.get("para") or 0
        self.para_deployed += para
    
    def EndTurn(self):
        self.isSuccess = self.IsSucess()
        super().EndTurn()

class Diaspora(Contract):
    ## kwargs : reference to the player, cm, tm, log


    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.reward = 2000
        self.gage = -200
        self.isSuccess = True
        self.name = "Diaspora I"
        self.difficulty = "Easy"
        self.description = f"Have at least one territory on each continent at the end of turn {self.expiration}"

    def IsSucess(self):
        continent_dict = self.tm.continent.continent_inverse

        territory_on_continent_count = {}
        NB_CONTINENT = 5
        for i in range(NB_CONTINENT):
            territory_on_continent_count[i] = 0

        for territory in self.tm.territories:
           if (territory.owner == self.player):
               continent_id = continent_dict[territory.id]
               territory_on_continent_count[continent_id] += 1

        res = all(value >= 1 for value in territory_on_continent_count.values())
        return(res)
    
    def EndTurn(self):
        self.isSuccess = self.IsSucess()
        super().EndTurn()


class DiasporaMedium(Contract):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.reward = 5000
        self.gage = -1500
        self.isSuccess = True
        self.name = "Diaspora II"
        self.difficulty = "Medium"
        self.description = f"Have at least two territories on each continent on turn {self.expiration}"

    def IsSucess(self):
        continent_dict = self.tm.continent.continent_inverse

        territory_on_continent_count = {}
        NB_CONTINENT = 5
        for i in range(NB_CONTINENT):
            territory_on_continent_count[i] = 0

        for territory in self.tm.territories:
           if (territory.owner == self.player):
               continent_id = continent_dict[territory.id]
               territory_on_continent_count[continent_id] += 1

        res = all(value >= 2 for value in territory_on_continent_count.values())
        return(res)
    
    def EndTurn(self):
        self.isSuccess = self.IsSucess()
        super().EndTurn()

class DiasporaHard(Contract):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.reward = 10000
        self.gage = -5000
        self.isSuccess = True
        self.name = "Diaspora III"
        self.difficulty = "Hard"
        self.description = f"Have at least three territories on each continent on turn {self.expiration}"

    def IsSucess(self):
        continent_dict = self.tm.continent.continent_inverse

        territory_on_continent_count = {}
        NB_CONTINENT = 5
        for i in range(NB_CONTINENT):
            territory_on_continent_count[i] = 0

        for territory in self.tm.territories:
           if (territory.owner == self.player):
               continent_id = continent_dict[territory.id]
               territory_on_continent_count[continent_id] += 1

        res = all(value >= 3 for value in territory_on_continent_count.values())
        return(res)
    
    def EndTurn(self):
        self.isSuccess = self.IsSucess()
        super().EndTurn()


class DraftContract:

    def __init__(self,**kwargs):
        
        self.name = None
        self.description = None
        self.expiration = 0
        self.arg = None
        self.tm = kwargs.get("tm") or None

        turn = kwargs.get("turn") or 0
        contract_name = kwargs.get("contract_name") or "Basic contract"

        if(contract_name == "Diaspora I"):
            self.name = "Diaspora I"
            self.expiration = turn + 4
            self.description = f"Have at least one territory on each continent at the end of turn {self.expiration}"
            self.arg = None

        if(contract_name == "Diaspora II"):
            self.name = "Diaspora II"
            self.expiration = turn + 4
            self.description = f"Have at least two territories on each continent at the end of turn {self.expiration}"
            self.arg = None

        if(contract_name == "Diaspora III"):
            self.name = "Diaspora III"
            self.expiration = turn + 4
            self.description = f"Have at least three territories on each continent at the end of turn {self.expiration}"
            self.arg = None

        if(contract_name == "Hold"):
            self.name = "Hold"
            self.expiration = turn + 4
            N = 46
            self.arg= rd.randint(0,N) 
            self.territory = self.tm.territories[self.arg]
            self.description = f"Hold territory {self.territory.name} at the end of turn {self.expiration}"

        

        if(contract_name == "Sailor"):
            self.name = "Sailor"
            self.expiration = turn + 4
            self.description = f"Deploy at least 5 navy troop before turn {self.expiration}"
            self.arg = None


        if(contract_name == "Aviator"):
            self.name = "Aviator"
            self.expiration = turn + 4
            self.description = f"Deploy at least 8 navy troop before turn {self.expiration}"
            self.arg = None
        
        if(contract_name == "MasterSeaAir"):
            self.name = "MasterSeaAir"
            self.expiration = turn + 4
            self.description = f"Deploy at least 10 navy troop and 10 para troop before end of turn {self.expiration}"
            self.arg = None

    def ToJson(self):
        json = {"name":self.name,"description": self.description,"arg":self.arg}
        return(json)