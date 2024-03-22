from attackmanager import AttackManager
from territorymanager import TerritoryManager
from territory import (Territory,TerritoryMultiple,TerritoryCard,TerritoryElephant,
                       TerritoryGorilla,TerritoryAlpaga,TerritoryCoati,TerritoryYack,
                       TerritoryChacal,TerritoryLama,TerritoryCoq,TerritoryFennec,TerritoryHyena,
                       TerritoryKoala,TerritoryMacaque,TerritoryParesseux,TerritoryPenguin,TerritoryTaipan,
                       TerritoryTapir,TerritoryZebra,TerritoryEagle,TerritoryPelican,TerritoryAlbatros,
                       TerritoryLion,TerritoryPanthera,TerritoryJaguar,TerritoryTurtle,TerritoryPangolin,TerritoryTatoo,
                       TerritoryDolphin,TerritoryCalmar,TerritoryShark,TerritoryBonobo,
                       TerritoryDragon,TerritoryHydra,TerritoryLicorne,TerritoryMinothaure,TerritoryDremadory,TerritoryWolf,
                       TerritoryFrog, TerritorySwan,TerritoryBear,TerritoryPaon)
from player import Player,Animal
import numpy as np
import random as rd
import pygame
from log import Log
from map import MAP
from contract import Contract,Stingy,Diaspora,Hold,Sailor,DraftContract
class CoreManager:

    def __init__(self,**kwargs):
        self.turn = 1
        self.players = kwargs["players"] or []
        self.log = kwargs["log"]
        self.am = AttackManager(self.log)
        self.tm = TerritoryManager() ## Not the actual tm, should be replace by None ?

        self.INIT(**kwargs)

        for p in self.players:
            p.InitiateGame(**{"tm":self.tm,"cm":self,"log" :self.log})
        for p in self.players:
            self.tm.SetConnectivity(p)
        self.actions = []
        self.am.continent = self.tm.continent
 

    def _Deploy(self,t:Territory,field,navy,para):
        owner = t.owner
        t.Deploy(**{"field":field,"navy":navy,"para":para})
        self.log.Info(f"Player {owner.name} deployed troops on territory {t.name}")
        owner.UpdateOnDeploy(**{"field":field,"navy":navy,"para":para})
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
            self.log.Log("No territory to deploy")
            return

        price = {"field": 1000,"navy":1500,"para":2000}
        cost = price["field"]*field + price["navy"]*navy + price["para"]*para
        t = self.tm.territories[territory]

        money = t.owner.money
        if(cost > money):
            
            print("Attempted to buy to many troops")
            self.log.Log("Attemped to buy to many troops")
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
            self.log.Log(f"Tried to attack from ally territories : {t0} and {t1}")
            return
        
        adjacent = self.tm.adjacent[t0,t1]
        
        way = self.tm.adjacent[t0,t1]
        if(not attacker.CanBattle(way)):
            print("Territory has no troop to attack")
            self.log.Log(f"Territory {t0} has no troop to attck {t1} by this way : {way}")
            return
        self._Attack(attacker,defender,way)
        return
    
    def Transfer(self,**kwargs):
        """Check if: the owner of the two territories are different
        The territory are adjacent
        The attackant have at least one troop available
        """

        t0_id = kwargs.get("t0")
        t1_id = kwargs.get("t1")
        field = kwargs.get("field")
        navy = kwargs.get("navy")
        para = kwargs.get("para")
        way = 2
        if(navy > 1):
            way = 1
        if(para> 1):
            way = 0
        kwargs = {"t0":t0_id,"t1":t1_id,"way":way,"compo":{"field":field,"navy":navy,"para":para}}
        possible = self.tm.TransferPossible(**kwargs)
        if(possible):
            self.log.Info(f"Player {self.tm.territories[t0_id].owner_name} transfered troop from {self.tm.territories[t0_id].name} to {self.tm.territories[t1_id].name}")
            self._Transfer(t0_id,t1_id,field,navy,para)
        else:
            print("Transfer was not possible ?")
            self.log.Log(f"Transfer on territory {t0_id} to {t1_id} was not possible.")
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
            self.log.Log(f"Player {player} attempted to buy discaerd card with not enough money")
            return
        self._DiscardCard(player)

    def SetContract(self,**kwargs):
        player_id = kwargs.get("player_id")
        player = self.players[player_id]
        player.SetContract(**kwargs)




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
        t.append(TerritoryLama(**{"name": "Territoire des Cactus Géants","id":1 ,"animals":animals}))
        t.append(TerritoryMultiple(**{"name": "Jungle 2","id":2 ,"animals":animals}))
        t.append(TerritoryCard(**{"name": "Territoire de la Nuit Sans Fin","id":3 ,"animals":animals}))
        t.append(TerritoryGorilla(**{"name": "Territoire de la Jungle Sauvage","id":4 ,"animals":animals}))
        t.append(TerritoryAlpaga(**{"name": "Territoire du Vaste Salar","id":5 ,"animals":animals}))
        t.append(TerritoryCoati(**{"name": "Territoire des Forets Luxuriantes","id":6 ,"animals":animals}))
        t.append(TerritoryYack(**{"name": "Territoire des Collines Verdoyantes","id":7 ,"animals":animals}))
        t.append(TerritoryElephant(**{"name": "Territoire des Volcans Etincelants","id":8 ,"animals":animals}))
        t.append(TerritoryZebra(**{"name": "Territoire Béni des Dieux","id":9 ,"animals":animals}))
        t.append(TerritoryAlbatros(**{"name": "Territoire des Cimes de l'Est","id":10 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryTapir(**{"name": "Territoires des Ruines Abandonées","id":11 ,"animals":animals}))
        t.append(TerritoryPenguin(**{"name": "Territoires des Aurores Boréales","id":12 ,"animals":animals}))
        t.append(TerritoryTaipan(**{"name": "Territoires du Désert Brulant","id":13 ,"animals":animals}))
        t.append(TerritoryCoq(**{"name": "Territoire Fleuri","id":14 ,"animals":animals}))
        t.append(TerritoryPanthera(**{"name": "Territoire de la Brousse Aride","id":15 ,"animals":animals,"tm":self.tm}))
        t.append(Territory(**{"name": "Jungle 16","id":16 ,"animals":animals}))
        t.append(TerritoryEagle(**{"name": "Territoire des Sommets Pointus","id":17 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryShark(**{"name": "Territoires des Iles Lointaines","id":18 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryDolphin(**{"name": "Territoires de la Mer Déchainée","id":19 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryChacal(**{"name": "Territories des Catacombes","id":20 ,"animals":animals}))
        t.append(TerritoryPelican(**{"name": "Territoires des Tempêtes","id":21 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryParesseux(**{"name": "Territoire de la Jungle Perdue","id":22 ,"animals":animals}))

        t.append(TerritoryCalmar(**{"name": "Territoires des Navires Echoués","id":23 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryBonobo(**{"name": "Territoire à la myriade d'Etoiles Filantes","id":24 ,"animals":animals,"tm":self.tm}))
        for i in range(25,26):
            t.append(Territory(**{"name": f"Jungle {i}","id":i ,"animals":animals}))

        t.append(TerritoryTatoo(**{"name": "Territoires de la Falaise Calcaire","id":26 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryTurtle(**{"name": "Territoire de la Plage de Darwin","id":27 ,"animals":animals,"tm":self.tm}))

        t.append(TerritoryJaguar(**{"name": "Territoire de la Foret Primaire","id":28 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryLion(**{"name": "Territoire de la Grande Savane","id":29 ,"animals":animals,"tm":self.tm}))


        t.append(Territory(**{"name": f"Territoires des Plaines Monotones","id":30 ,"animals":animals}))
        t.append(TerritoryPangolin(**{"name": "Terriotires des Grottes Escarpées","id":31 ,"animals":animals,"tm":self.tm}))
        ##t.append(TerritoryGlutton(**{"name": "Territoire de la la météo lunatique","id":32 ,"animals":animals,"tm":self.tm}))
        t.append(Territory(**{"name": "Territoire des nuages appaisants","id":32 ,"animals":animals,"tm":self.tm}))

        for i in range(33,34):
            t.append(Territory(**{"name": f"Jungle {i}","id":i ,"animals":animals}))
        ##t = kwargs["territories"]
            
        t.append(TerritoryHydra(**{"name": "Territoires des Marécage Brumeux","id":34 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryMinothaure(**{"name": "Territoires du Labyrinthe Perdu","id":35 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryDremadory(**{"name": "Territoires des Canyons Serpentants","id":36 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryLicorne(**{"name": "Territoires de la Foret Argentée","id":37 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryPaon(**{"name": "Territoires des Tempêtes du Matin","id":38 ,"animals":animals}))
        t.append(TerritoryDragon(**{"name": "Territoires des Grottes Flamboyantes","id":39 ,"animals":animals,"tm":self.tm}))
        t.append(TerritoryFrog(**{"name": "Territoires des Marais Mauves","id":40 ,"animals":animals,"tm":self.tm}))
        t.append(TerritorySwan(**{"name": "Territoires du Lac Majesteux","id":41 ,"animals":animals,"tm":self.tm}))
        for i in range(42,43):
            t.append(Territory(**{"name": f"Jungle {i}","id":i ,"animals":animals}))

        t.append(Territory(**{"name": "Jungle 43","id":43 ,"animals":animals}))
        t.append(TerritoryBear(**{"name": f"Territoires au bord du Grand Précipice","id":44 ,"animals":animals}))
        t.append(TerritoryWolf(**{"name": "Territoires de la Météo Lunatique","id":45 ,"animals":animals,"tm":self.tm}))
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
                ##t[i].owner_id = owners[i]
                ##t[i].owner = self.players[owners[i]]
                t[i].SetOwner(self.players[owners[i]])
                t[i].troop["field"] = 2
            else:
                t[i].owner = animals
                t[i].owner_id = -1
                t[i].owner_name = "animals"
                t[i].troop = {"field":0,"navy":0,"para":0,"animals":t[i].maxAnimals}

        
        for terr in t:
            terr.log = self.log

        self.tm = TerritoryManager(territories = t)


        # Should be removed and have better logic
        for i in range(45):
            t[i].tm = self.tm


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
        action_dict = {"Attack":self.Attack,"Deploy":self.Deploy,"Transfer":self.Transfer,"DiscardCard":self.DiscardCard,"SetContract":self.SetContract}
        for action in filter(lambda act: (act.name in ["SetContract"]),self.actions):
            print("Executing the following action :")
            action.print()
            self.log.Log(f"Executing action {action.name} : {action.args}")
            func = action_dict.get(action.name)
            func(**action.args)
        for action in filter(lambda act: (act.name in ["Deploy","Transfer","DiscardCard"]),self.actions):
            print("Executing the following action :")
            action.print()
            self.log.Log(f"Executing action {action.name} : {action.args}")
            func = action_dict.get(action.name)
            func(**action.args)

        for action in filter(lambda act: (act.name in ["Attack"]),self.actions):
            print("Executing the following action :")
            action.print()
            self.log.Log(f"Executing action {action.name} : {action.args}")   
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
        res["contracts"] = []
        for player in self.players:
            res["players"].append(player.ToJson())
       
        return(res)
    
    def StaticTerritoriesToJson(self):
        res = self.tm.ToStaticJson()
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


            



    