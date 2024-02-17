from player import Player
from coremanager import CoreManager
from action import Action
import random as rd

class Bot:
    N_TERRITORY = 16
    def __init__(self,p:Player,cm:CoreManager):
        self.player = p
        self.cm = cm

    def GetAction(self):
        # First we get deployment
        act = []
        terr = self.cm.GetTerritory(self.player.id)
        money = self.player.money
        price = {"field": 1000,"navy":1200,"para":1500}
        troopToDeploy = {"field": 0,"navy":0,"para":0}
        if(terr):
            randomterr = rd.choice(terr).id
            troopToDeploy["t0"] = randomterr
            while(money > 1500):
                ##troop,value = rd.choice(list(price.items()))
                i = rd.randint(0,10)
                if(i <= 5):
                    troop,value = "field",1000
                elif(i<=8):
                    troop,value = "navy", 1200
                else:
                    troop,value = "para",1500

                troopToDeploy[troop] += 1
                money-= value

            act.append(Action("Deploy",**troopToDeploy))

            randomterrAttack = rd.choice(terr).id
            randomterrDef = rd.choice(self.cm.tm.territories).id
            if(rd.random()<0.20):
                randomterrDed = 11
            act.append(Action("Attack",t0 = randomterrAttack,t1 = randomterrDef))
            for a in act:
                a.print()
        return(act)
        

class CleverBot(Bot):

    def __init__(self,p:Player,cm:CoreManager):
        super().__init__(p,cm)

    def GetAction(self):
        # First we get deployment
        act = []
        terr = self.cm.GetTerritory(self.player.id)
        money = self.player.money
        price = {"field": 1000,"navy":1200,"para":1500}
        troopToDeploy = {"field": 0,"navy":0,"para":0}
        if(terr):
            randomterr = rd.choice(terr).id
            troopToDeploy["t0"] = randomterr
            while(money > 1500):
                ##troop,value = rd.choice(list(price.items()))
                i = rd.randint(0,10)
                if(i <= 6):
                    troop,value = "field",1000
                elif(i<=9):
                    troop,value = "navy", 1200
                else:
                    troop,value = "para",1500

                troopToDeploy[troop] += 1
                money-= value

            act.append(Action("Deploy",**troopToDeploy))

            # Here we improve the way the territroy to attack is choosen
            """choices = []
            for t in terr:
                choices.append(t)
                if(t.CountTroop()> 6):
                    choices.append(t)
                    choices.append(t)
                    choices.append(t)
                    choices.append(t)
            randomterrAttack = rd.choice(choices).id"""
            randomterrAttack = self.SmartAttackFromChoice()
            randomterrDef = self.SmartAttackToChoice(randomterrAttack)

            """choices = []
            for t in self.cm.tm.territories:
                choices.append(t)
                if(self.cm.tm.adjacent[t.id,randomterrAttack] == 2):
                    choices.append(t)
                    choices.append(t)
                    choices.append(t)
                    choices.append(t)

                if(t.id == 11):
                    choices.append(t)
                    choices.append(t)
                
            randomterrDef = rd.choice(choices).id"""
            act.append(Action("Attack",t0 = randomterrAttack,t1 = randomterrDef))
        return(act)
    
    def DumbAttackFromChoice(self):
        terr = self.cm.GetTerritory(self.player.id)
        randomterr = rd.choice(terr).id
        return(randomterr)

    def SmartAttackFromChoice(self):
        terr = self.cm.GetTerritory(self.player.id)
        weights = []
        for t in terr:
            weight = t.CountTroop()
            weights.append(weight)

        randomterr = rd.choices(terr,weights = weights)[0].id
        return(randomterr)
    
    def DumbAttackToChoice(self,fr):
        randomterr = rd.choice(self.cm.tm.territories).id
        return(randomterr)

    def SmartAttackToChoice(self,fr):
        weights = []
        for t in self.cm.tm.territories:
            if(self.cm.tm.adjacent[t.id,fr] == 2 and t.owner_id != self.player.id):
                weight = 5
            else:
                weight = 1
            weights.append(weight)
        randomterr = rd.choices(self.cm.tm.territories,weights = weights)[0].id
        return(randomterr)

        
                

