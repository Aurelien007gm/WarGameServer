class Continent :

    def __init__(self,**kwargs):
        self.continent = {0:range(0,12),1:range(12,18),2:range(18,23),3:range(23,32)}
        self.continent_inverse = {}
        self.ComputeInverse()
        self.tm = kwargs.get("tm")

    def ComputeInverse(self):
        for continent, territories in self.continent.items():
            for t in territories:
                self.continent_inverse[t] = continent


    def Reward(self):
        for continent, territories in self.continent.items():
            owner = self.tm.territories[territories[0]].owner_id
            owned = (owner>= 0)
            for t in territories:
                if(self.tm.territories[t].owner_id != owner):
                    owned = False
            
            # Custom logic for specific map, should be modified
            if(owned):
                if(continent != 2):
                    self.tm.territories[territories[0]].owner.AddMoney(1000)
                else:
                    self.tm.territories[territories[0]].owner.AddMoney(200)

            
    def HasContinent(self,player:int,t:int):
        res = True
        c = self.continent_inverse[t]
        for t_id in self.continent[c]:
            terr = self.tm.territories[t_id]
            if (terr.owner_id!= player):
                print(terr.id)
                print(terr.owner_id)
                print(player)

                res = False
                break
        return(res)