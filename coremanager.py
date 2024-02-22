from attackmanager import AttackManager
from territorymanager import TerritoryManager
from territory import (Territory,TerritoryMultiple,TerritoryCard,TerritoryElephant,
                       TerritoryGorilla,TerritoryAlpaga,TerritoryCoati,TerritoryYack,
                       TerritoryChacal,TerritoryLama,TerritoryCoq,TerritoryFennec,TerritoryHyena,
                       TerritoryKoala,TerritoryMacaque,TerritoryParesseux,TerritoryPenguin,TerritoryTaipan,
                       TerritoryTapir,TerritoryZebra)
from player import Player,Animal
import numpy as np
import random as rd
import pygame

from map import MAP
class CoreManager:

    def __init__(self,**kwargs):
        self.players = kwargs["players"] or []
        ##self.players.append(Player(**{"name":"Arnaud","id":0}))
        ##self.players.append(Player(**{"name":"Aurélien","id":1}))
        self.am = AttackManager()
        self.tm = TerritoryManager()
        self.INIT(**kwargs)
        for p in self.players:
            self.tm.SetConnectivity(p)
        self.actions = []
        self.am.continent = self.tm.continent
        self.turn = 1

    def _Deploy(self,t:Territory,field,navy,para):
        owner = t.owner
        t.Deploy(**{"field":field,"navy":navy,"para":para})
        price = {"field": 1000,"navy":1500,"para":2000}
        owner.AddMoney(-price["field"]*field)
        owner.AddMoney(-price["navy"]*navy)
        owner.AddMoney(-price["para"]*para)

    def Deploy(self,**kwargs):
        territory = kwargs.get("t0")
        field = kwargs.get("field") or 0
        navy = kwargs.get("navy") or 0
        para = kwargs.get("para") or 0
        if(territory is None):
            print("No territory to deploy")
            return

        price = {"field": 1000,"navy":1500,"para":2000}
        cost = price["field"]*field + price["navy"]*navy + price["para"]*para
        t = self.tm.territories[territory]

        money = t.owner.money
        if(cost > money):
            
            print("Attempted to buy to many troop")
            return
        self._Deploy(t,field,navy,para)

    def Begin(self):
        for t in self.tm.territories:
            t.BeginTurn()
        return


    def _Attack(self,t0:Territory,t1:Territory,way):
        self.am.Attack(**{"attacker":t0,"defender":t1,"way":way})

    def Attack(self,**kwargs):
        """Check if: the owner of the two territories are different
        The territory are adjacent
        The attackant have at least one troop available
        """
        t0 = kwargs.get("t0")
        t1 = kwargs.get("t1")
        attacker = self.tm.territories[t0]
        defender = self.tm.territories[t1]
        if(attacker.owner_id == defender.owner_id):
            print("Tried to attack from ally territories")
            return
        
        adjacent = self.tm.adjacent[t0,t1]
        
        way = self.tm.adjacent[t0,t1]
        if(not attacker.CanBattle(way)):
            print("Territory has no troop to attack")
            return
        self._Attack(attacker,defender,way)
        return
    
    def Transfer(self,**kwargs):
        """Check if: the owner of the two territories are different
        The territory are adjacent
        The attackant have at least one troop available
        """

        t0 = kwargs.get("t0")
        t1 = kwargs.get("t1")
        field = kwargs.get("field")
        navy = kwargs.get("navy")
        para = kwargs.get("para")
        way = 2
        if(navy > 1):
            way = 1
        if(para> 1):
            way = 0
        kwargs = {"t0":t0,"t1":t1,"way":way,"compo":{"field":field,"navy":navy,"para":para}}
        possible = self.tm.TransferPossible(**kwargs)
        if(possible):
            self._Transfer(t0,t1,field,navy,para)
        else:
            print("Transfer was not possible ?")
        return



    def _Transfer(self,t0,t1,field,navy,para):
        self.tm.Transfer(t0,t1,{"field":field,"navy":navy,"para":para})

    def SetOwner(self,t,p):
        self.tm.territories[t].owner = self.players[p]

    def _DiscardCard(self,p):
        self.players[p].DiscardCard(100)

    def DiscardCard(self,**kwargs):
        player = kwargs.get("player")
        cost = 100
        p = self.players[player]
        money = p.money
        if(cost > money):
            print("Attempted to buy to discard card while not enough money")
            return
        self._DiscardCard(player)

    def EndTurn(self):
        for t in self.tm.territories:
            t.BeforeEnd()

            reward = t.Reward()
            owner = t.owner
            owner.AddMoney(reward)
            t.EndTurn()

        for p in self.players:
            p.EndTurn()

        #self.tm.continent.Reward()

    """def BeginTurn(self):
        self.turn += 1
        if(self.turn == 1):
            return
        for t in self.tm.territories:

            reward = t.Reward()
            owner = t.owner
            owner.AddMoney(reward)
            t.EndTurn()"""

    def INIT(self,**kwargs):
        t = []
        animals = Animal()
        """
        for i in range(16):
            if(i== 11):
                terr = TerritoryMultiple(**{"name": "Territoire des arbres centenaires "+str(i),"id": i,"animals":animals})
            elif(i==8):
                terr = TerritoryCard(**{"name": "Territoire de la nuit sans fin "+str(i),"id": i,"animals":animals})
            elif(i==15):
                terr = TerritoryGorilla(**{"name": "Territoire de la jungle sauvage "+str(i),"id": i,"animals":animals})
            elif(i==9):
                terr = TerritoryAlpaga(**{"name": "Territoire du vaste Salar "+str(i),"id": i,"animals":animals})
            elif(i==6):
                terr = TerritoryCoati(**{"name": "Territoire du vaste Salar "+str(i),"id": i,"animals":animals})
            elif(i==4):
                terr = TerritoryYack(**{"name": "Territoire des collines verdiyante "+str(i),"id": i,"animals":animals})
            elif(i==2):
                terr = TerritoryElephant(**{"name": "Territoire des volcants étincelants "+str(i),"id": i,"animals":animals})
            else:
                terr = Territory(**{"name": "Jungle "+str(i),"id": i,"animals":animals})
            t.append(terr)"""
        
        t.append(Territory(**{"name": "Jungle 0","id":0 ,"animals":animals}))
        t.append(TerritoryLama(**{"name": "Jungle 1","id":1 ,"animals":animals}))
        t.append(TerritoryMultiple(**{"name": "Jungle 2","id":2 ,"animals":animals}))
        t.append(TerritoryCard(**{"name": "Jungle 3","id":3 ,"animals":animals}))
        t.append(TerritoryGorilla(**{"name": "Jungle 4","id":4 ,"animals":animals}))
        t.append(TerritoryAlpaga(**{"name": "Jungle 5","id":5 ,"animals":animals}))
        t.append(TerritoryCoati(**{"name": "Jungle 6","id":6 ,"animals":animals}))
        t.append(TerritoryYack(**{"name": "Jungle 7","id":7 ,"animals":animals}))
        t.append(TerritoryElephant(**{"name": "Jungle 8","id":8 ,"animals":animals}))
        t.append(TerritoryZebra(**{"name": "Jungle 9","id":9 ,"animals":animals}))
        t.append(TerritoryChacal(**{"name": "Jungle 10","id":10 ,"animals":animals}))
        t.append(TerritoryTapir(**{"name": "Jungle 11","id":11 ,"animals":animals}))
        t.append(TerritoryPenguin(**{"name": "Jungle 12","id":12 ,"animals":animals}))
        t.append(TerritoryTaipan(**{"name": "Jungle 13","id":13 ,"animals":animals}))
        t.append(TerritoryCoq(**{"name": "Jungle 14","id":14 ,"animals":animals}))
        t.append(TerritoryParesseux(**{"name": "Jungle 15","id":15 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 16","id":16 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 17","id":17 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 18","id":18 ,"animals":animals}))
        t.append(Territory(**{"name": "Jungle 19","id":19 ,"animals":animals}))

        for i in range(20,32):
            t.append(Territory(**{"name": f"Jungle {i}","id":i ,"animals":animals}))
        ##t = kwargs["territories"]
        nbterritory = len(t)
        nbPlayer = len(self.players)
        territoryPerPlayer = nbterritory//nbPlayer
        remainder =  nbterritory % nbPlayer
        owners = []
        for p in self.players:
            for i in range(territoryPerPlayer):
                owners.append(p.id)
        
        for r in range(remainder):
            owners.append(-1)

    
        rd.shuffle(owners)
        for i in range(nbterritory):
            if(owners[i]) >= 0:
                t[i].owner_id = owners[i]
                t[i].owner = self.players[owners[i]]
                t[i].troop["field"] = 2
            else:
                t[i].owner = animals
                t[i].owner_id = -1
                t[i].owner_name = "animals"
                t[i].troop = {"field":0,"navy":0,"para":0,"animals":self.maxAnimals}

        self.tm = TerritoryManager(territories = t)
        self.tm.adjacent = MAP
            

    def print(self):
        for p in self.players:
            p.print()

        for t in self.tm.territories:
            t.print()

    def SetAction(self,action):
        self.actions.append(action)

    def Run(self):
        rd.shuffle(self.actions)
        self.actions.sort(key = lambda t:t.value)
        action_dict = {"Attack":self.Attack,"Deploy":self.Deploy,"Transfer":self.Transfer,"DiscardCard":self.DiscardCard}
        for action in filter(lambda act: (act.name in ["Deploy","Transfer","DiscardCard"]),self.actions):
            print("Executing the following action :")
            action.print()
            func = action_dict.get(action.name)
            func(**action.args)

        for action in filter(lambda act: (act.name in ["Attack"]),self.actions):
            print("Executing the following action :")
            action.print()
            func = action_dict.get(action.name)
            func(**action.args)
        self.actions = []
        self.EndTurn()
        for p in self.players:
            self.tm.SetConnectivity(p)
        self.turn += 1

    def GetTerritory(self,p:int):
        terr = []
        for t in self.tm.territories:
            if(t.owner_id == p):
                terr.append(t)

        return(terr)
    
    def ToJson(self):
        res = self.tm.ToJson()
        res["turn"] = self.turn
        res["players"] = []
        for player in self.players:
            res["players"].append(player.ToJson())
        return(res)
    
    def Validate(self,p):
        run = True
        self.players[p].Validate()
        for player in self.players:
            print(player.id,player.isbot,player.ready)
            if not player.ready:
                run = False
                print(f"player{player.name} is not ready")
        if(run):
            print("All player ready")
        else:
            print("Not all player are ready")
        return(run)


            



    