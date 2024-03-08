import random as rd
from card import Card
from contract import Contract,Stingy,Diaspora,DiasporaMedium,DiasporaHard,Hold,Sailor,DraftContract,MasterSeaAir,Aviator
from log import Log
class Player:

    def __init__(self,**kwargs):
        self.money = 5000
        self.name = kwargs.get("name") or "Unknown"
        self.id = kwargs.get("id") or 0
        self.tm = None
        self.color = kwargs.get("color") or (127,127,127)
        self.cards = []
        self.contract= None
        self.cm = None
       
        self.isbot = kwargs.get("isbot")
        self.log = kwargs.get("log") or Log()
        self.ready = self.isbot
        self.contracts_drawn = []
 
        for i in range(10):
            self.cards.append(Card())


    def InitiateGame(self,**kwargs):
        self.tm = kwargs["tm"]
        self.cm = kwargs["cm"]
        self.log = kwargs["log"]
        self.DrawDraftContract()



    def AddMoney(self,nb):
        self.money+= nb
        if(nb < 0):
            if self.contract :
                self.contract.Fail("MoneySpend")

    def print(self):
        print("Player "+ self.name +" has " + str(self.money) )
        print("Player Cards are " )
        for c in self.cards:
            c.print()

    def Validate(self):
        self.ready = True

    def DiscardCard(self,cost = None):
        self.cards.sort(key=lambda t:t.attack + t.defense)
        print("Discard card")
        self.cards[0].print()
        self.cards[0] = Card()
        print("Get ")
        self.cards[0].print()
        if(cost):
            self.money -= cost

    def DrawCard(self):
        i = rd.randint(0,9)
        card = self.cards[i]
        self.cards[i] = Card()
        self.cards.sort(key=lambda t:t.attack + t.defense)
        return(card)
    
    def EndTurn(self):
        if self.contract:
            self.contract.Print()
            self.contract.EndTurn()
        if (self.contract):
            self.contract = self.contract if not self.contract.CheckDelete() else None

        self.DrawDraftContract()


        if(not self.isbot):
            self.ready = False

    def DrawContract(self):
        contract = Sailor(**{"log":self.log,"tm":self.tm,"player":self,"cm":self.cm})
        contract.Print()
        self.contract = contract


    def DrawDraftContract(self):
        # return three
        turn = self.cm.turn
        contracts_easy = []
        contracts_easy.append(DraftContract(**{"contract_name":"Diaspora I","turn":turn}))
        contracts_easy.append(DraftContract(**{"contract_name":"Sailor","turn":turn}))
        contracts_easy.append(DraftContract(**{"contract_name":"Hold","turn":turn,"tm":self.tm}))

        contracts_medium = []
        contracts_medium.append(DraftContract(**{"contract_name":"Aviator","turn":turn}))
        contracts_medium.append(DraftContract(**{"contract_name":"Diaspora II","turn":turn}))
        
        contracts_hard = []
        contracts_hard.append(DraftContract(**{"contract_name":"MasterSeaAir","turn":turn}))
        contracts_hard.append(DraftContract(**{"contract_name":"Diaspora III","turn":turn}))
        self.contracts_drawn = [rd.choice(contracts_easy),rd.choice(contracts_medium),rd.choice(contracts_hard)]


    def ToJson(self):
        # return a json reprensenting a player
        res = {"name" : self.name,"id":self.id,"money":self.money,"cards":[],"contract":None}

        for c in self.cards:
            res["cards"].append(c.ToJson())

        if self.contract:
            res["contract"] = self.contract.ToJson()

        res["contracts_drawn"] = []
        for c in self.contracts_drawn:
            res["contracts_drawn"].append(c.ToJson())

        return(res)
    
    def UpdateOnDeploy(self,**kwargs):
        ## Update contracts that involve deploying troops 
        if(self.contract):
            self.contract.UpdateOnDeploy(**kwargs)

    def SetContract(self,**kwargs):
        contract_name = kwargs.get("contract_name")
        arg = kwargs.get("arg") or None
        cm = self.cm
        tm = self.tm
        log = self.log
        kwargs = {"cm":cm,"tm":tm,"player":self,"arg": arg,"log":self.log}
        contract_construct = {"Sailor": Sailor,"MasterSeaAir":MasterSeaAir,"Diaspora":Diaspora,"Aviator":Aviator,
                              "Diapora II":DiasporaMedium,"Diaspora III":DiasporaHard,"Hold":Hold}
        self.contract = contract_construct[contract_name](**kwargs)


    
class Animal(Player):

    def __init__(self,**kwargs):
        self.money = 0
        self.name = "animals"
        self.id = -1
        self.cards = []
        self.color = (200,200,100)

    def AddMoney(self,nb):
        return

    def print(self):
        print("Animals")

    def DiscardCard(self,cost = None):
        return

    def DrawCard(self):
        return(Card())