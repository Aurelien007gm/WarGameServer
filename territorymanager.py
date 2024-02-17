import numpy as np
from continent import Continent

class TerritoryManager:

    def __init__(self,**kwargs):
        self.territories = kwargs.get("territories") or []
        self.continent = Continent(tm = self)
        self.nb_territory = len(self.territories)
        
        self.adjacent = np.zeros((len(self.territories),len(self.territories)))
        self.connectivity = {}

    def ComputeConnectedMatrix(self,player:int):
        new = np.zeros((self.nb_territory,self.nb_territory))
        for i in range(self.nb_territory):
            for j in range(self.nb_territory):
                if ((self.territories[i].owner == player) and (self.territories[j].owner == player)):
                    new[i,j] = self.adjacent[i,j]

        nbIter = self.CountTerritory(player)
        playerTerritories = self.GetPlayerTerritories(player)

        for i in range (nbIter):
            old = np.copy(new)
            new = np.zeros((self.nb_territory,self.nb_territory))

            for t0 in playerTerritories:
                for t1 in playerTerritories:
                    for tinter in playerTerritories:
                        val = max(old[t0,t1],min(old[t0,tinter],old[tinter,t1])) 
                        new[t0,t1] = max(val,new[t0,t1])

        return(new)



    def CountTerritory(self,player:int):
        count:int  = 0
        for territory in self.territories:
            if territory.owner == player:
                count+=1
        return(count)
    
    def GetPlayerTerritories(self,player:int):
        res = []
        for territory in self.territories:
            if territory.owner == player:
                res.append(territory.id)
        return(res)
    
    def SetConnectivity(self,player:int):
        self.connectivity[player] = self.ComputeConnectedMatrix(player)

    def TransferPossible(self,**kwargs):
        t0:int = kwargs["t0"]
        t1:int = kwargs["t1"]
        way:int = kwargs["way"]
        compo = kwargs["compo"]
        res = True
        if(self.territories[t0].owner != self.territories[t1].owner):
            res = False
        else:
            player = self.territories[t0].owner
            w = self.connectivity[player][t0][t1]
            res = (w >= way)

        for key,value in compo.items():
            if(self.territories[t0].troop[key]< value):
                res = False

        return(res)
    
    
    def Transfer(self,t0,t1,compo):
        for key,value in compo.items():
            self.territories[t0].troop[key] -= value
            self.territories[t1].troop[key] += value

    def Add(self,t,compo):
        for key,value in compo.items():
            t.troop[key] -= value

    def ToJson(self):
        print("hey2")
        result = {"territories": []}

        for territory in self.territories:
            territory.print()
            print("...")
            print(territory.ToJson())
            result["territories"].append(territory.ToJson())

        return result

    

