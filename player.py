import random as rd
from card import Card
from contract import Contract,Stingy
class Player:

    def __init__(self,**kwargs):
        self.money = 5000
        self.name = kwargs.get("name") or "Unknown"
        self.id = kwargs.get("id") or 0
        self.color = kwargs.get("color") or (127,127,127)
        self.cards = []
        self.contracts = []
        for i in range(10):
            self.cards.append(Card())
        self.DrawContract()



    def AddMoney(self,nb):
        self.money+= nb
        if(nb < 0):
            for contract in self.contracts:
                contract.Fail("MoneySpend")

    def print(self):
        print("Player "+ self.name +" has " + str(self.money) )
        print("Player Cards are " )
        for c in self.cards:
            c.print()

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
        for contract in self.contracts:
            contract.Print()
            contract.EndTurn()
        self.contracts = [c for c in self.contracts if not c.CheckDelete()]
    def DrawContract(self):
        contract = Stingy()
        contract.player = self
        contract.Print()
        self.contracts.append(contract)

    def ToJson(self):
        res = {"name" : self.name,"money":self.money,"cards":[],"contracts":[]}

        for c in self.cards:
            res["cards"].append(c.ToJson())

        for c in self.contracts:
            res["contracts"].append(c.ToJson())

        return(res)


    
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