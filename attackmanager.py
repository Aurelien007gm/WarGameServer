from territory import Territory

class AttackManager:
    DEBUG = True

    def __init__(self):
        self.tm = None


    def Wave(self,**kwargs):
        DEBUG = True
        attacker : Territory = kwargs.get("attacker")
        defender : Territory = kwargs.get("defender")
        attackcompo : list = kwargs.get("attackcompo")
        defensecompo :list  = kwargs.get("defensecompo")


        nbAttacker : int = len(attackcompo)
        nbDefender : int = len(defensecompo)
        nbAttack = min(nbAttacker,nbDefender)

        attackerLoss = 0
        defenderLoss = 0

        attackCards : list =attacker.DrawCards(nbAttacker)
        attackCards.sort(key =lambda x: x.attack,reverse = True)
        defenseCards: list =defender.DrawCards(nbDefender)
        defenseCards.sort(key= lambda x: x.defense,reverse = True)

        if(DEBUG):
            for card in attackCards:
                card.print()
            print("====")
            for card in defenseCards:
                card.print()

        for i in range(nbAttack):
            attack = attackCards[i].attack
            defense = defenseCards[i].defense
            if(attack <= defense):
                attackerLoss += 1
            else:
                defenderLoss += 1
        kwargs["attackerLoss"] = attackerLoss
        kwargs["defenderLoss"] = defenderLoss
        attacker.LooseTroop(attackerLoss,attackcompo)
        defender.LooseTroop(defenderLoss,defensecompo)
        return(kwargs)

    def Attack(self,**kwargs):
        DEBUG = True
        attacker : Territory = kwargs.get("attacker")
        attacker.SetMaxTroop()
        defender : Territory = kwargs.get("defender")
        hasContinent = self.continent.HasContinent(defender.owner_id,defender.id)
        print("Setting max troop")
        defender.SetMaxTroop(hasContinent)
        way: int = kwargs.get("way")

        maxIter: int = 100
        iteration = 0
        if(defender.hasbeentaken or attacker.hasbeentaken):
            print("One of the territory has been taken this turn")
            return
        
        if(defender.CancelSpecial()):
            print("Attack was cancelled")
            return
        while attacker.CanBattle(way,True) and defender.CanBattle(way,False) and iteration  <maxIter:
            if(DEBUG):
                attacker.print()
                defender.print()
            attacker.hasAttacked = True
            kwargs["attackcompo"] = attacker.GetCompo(way,True)
            kwargs["defensecompo"] = defender.GetCompo(way,False)
            kwargs = self.Wave(**kwargs)
            iteration += 1
        
        if not defender.CanBattle(way,False):
            defender.Conquest(**kwargs)
            remaining = kwargs["attackcompo"][kwargs["attackerLoss"]:]
            for r in remaining:
                attacker.troop[r] -= 1
                defender.troop[r] +=1
            
        

        if(DEBUG):
            attacker.print()
            defender.print()






