##from data.map import MapData
from territory import Territory
from attackmanager import AttackManager
import numpy as np
from territorymanager import TerritoryManager

##def test():
  ##  data = MapData

def testWave():
    print("====Début du test====")
    t0 = Territory(**{"name": "Jungle Maléfique","id": 1})
    t1 = Territory(**{"name": "Brousse argente","id": 2})
    t0.troop = ({"field":5,"navy":1,"para":0,"animals":0})
    t1.troop = ({"field":4,"navy":1,"para":0,"animals":0})
    t0.print()
    t1.print()
    att = AttackManager()
    att.Wave(**{"attacker":t0,"defender":t1,
              "attackcompo":["field","field","field"],"defensecompo":["field","field"]})

    t0.print()
    t1.print()

def testCompo():
    t0 = Territory(**{"name": "Jungle Maléfique","id": 1})
    t0.owner = 1
    t0.troop = ({"field":1,"navy":1,"para":1,"animal":0})
    compo = t0.GetCompo(2,True)
    print(compo == ["field","navy","para"])
    compo = t0.GetCompo(1,True)
    print(compo == ["navy","para"])
    compo = t0.GetCompo(0,True)
    print(compo == ["para"])

    t0.troop = ({"field":2,"navy":1,"para":2,"animal":0})
    compo = t0.GetCompo(2,True)
    print(compo == ["field","field","navy"])
    compo = t0.GetCompo(1,True)
    print(compo == ["navy","para","para"])
    compo = t0.GetCompo(0,True)
    print(compo == ["para","para"])

def testAttack():
    print("====Début du test====")
    t0 = Territory(**{"name": "Jungle Maléfique","id": 1})
    t1 = Territory(**{"name": "Brousse argente","id": 2})
    t0.owner = 1
    t1.owner = 2
    t0.troop = ({"field":7,"navy":5,"para":4,"animals":0})
    t1.troop = ({"field":4,"navy":1,"para":4,"animals":0})
    att = AttackManager()
    att.Attack(**{"attacker":t0,"defender":t1,"way": 1})

    t0.print()
    t1.print()

def testConnectivity():
    t = []
    for i in range(7):
        terr = Territory(**{"name": "Jungle"+str(i),"id": i})
        terr.owner = 1
        t.append(terr)
    t[4].owner = 2
    connec = np.array([[2,2,0,0,0,0,0],
                      [2,2,2,0,2,0,0],
                      [0,2,2,0,0,0,0],
                      [0,0,0,2,2,0,0],
                      [0,2,0,2,2,0,0],
                      [0,0,0,0,0,2,1],
                      [0,0,0,0,0,1,2]])
    
    tm = TerritoryManager(**{"territories" :t})
    tm.adjacent = connec
    tm.territories = t
    tm.nb_territory = 7
    print(tm.territories)
    print(tm.adjacent)
    mat = tm.ComputeConnectedMatrix(1)
    print(mat)



def main():
    ###testWave()
    ###testCompo()
    ###testAttack()
    testConnectivity()
main()

