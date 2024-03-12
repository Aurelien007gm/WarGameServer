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
        print("===========")
        print(self.nb_territory)
        print(len(self.territories))
        print(len(self.adjacent))
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
        t0_id:int = kwargs["t0"]
        t1_id:int = kwargs["t1"]
        way:int = kwargs["way"]
        compo = kwargs["compo"]
        res = True
        if(self.territories[t0_id].owner != self.territories[t1_id].owner):
            res = False
        else:
            player = self.territories[t0_id].owner
            w = self.connectivity[player][t0_id][t1_id]
            res = (w >= way)

        for key,value in compo.items():
            if(self.territories[t0_id].troop[key]< value):
                res = False

        return(res)
    
    
    def Transfer(self,t0_id,t1_id,compo):
        for key,value in compo.items():
            self.territories[t0_id].troop[key] -= value
            self.territories[t1_id].troop[key] += value

    def Add(self,t,compo):
        for key,value in compo.items():
            t.troop[key] -= value

    def ToJson(self):
        result = {"territories": []}

        for territory in self.territories:
            result["territories"].append(territory.ToJson())

        return result
    
    def ToStaticJson(self):
        # Do not includes troop on territories but include effect
        # Return a list, without the labal territories
        result = []

        for territory in self.territories:
            result.append(territory.ToStaticJson())
        return result
    
    def HaveBird(self,player_id):

        # Check ids are correct if you changes territories
        ids = [10,17,21]
        res = True
        for id in ids:
            if (self.territories[id].owner_id != player_id):
                res = False

        return(res)
    

    def HaveFish(self,player_id):

        # Check ids are correct if you changes territories
        ids = [18,19,23]
        res = True
        for id in ids:
            if (self.territories[id].owner_id != player_id):
                res = False

        return(res)
    

    def HaveFelins(self,player_id):

        # Check ids are correct if you changes territories
        ids = [15,28,29]
        res = True
        for id in ids:
            if (self.territories[id].owner_id != player_id):
                res = False

        return(res)
    
    def CountMythical(self,player_id):

        # Check ids are correct if you changes territories
        ids = [34,35,37,39]
        res = 0
        for id in ids:
            if (self.territories[id].owner_id != player_id):
                res += 1

        return(res)
    
    def CountAdjacent(self,player_id,adjacent_ids):
        #Count adjacent territories owned by player

        
        count = 0
        for territory_id in adjacent_ids:
            if (player_id == self.territories[territory_id].owner_id):
                count += 1

        return(count)


    

