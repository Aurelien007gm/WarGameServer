import random as rd

class Card:

    def __init__(self,attack = None,defense = None):
        self.attack = attack or rd.randint(1,6)
        self.defense = defense or rd.randint(1,6)

    def print(self):
        print("Attaque : "+ str(self.attack) + " ,Defense : " +str(self.defense))


