from coremanager import CoreManager
from bot import Bot, CleverBot
from action import Action
from player import Player

# Main instance of a game
class Game:
    def __init__(self,bot = True):
        self.players = []
        self.bots =[]
        self.players.append(Player(**{"name":"Bot","id":0,"color":(0,0,255)}))
        self.players.append(Player(**{"name":"SuperBot","id":1,"color":(0,255,0)}))
        self.players.append(Player(**{"name":"Aurélien","id":2,"color":(255,0,0)}))
        self.players.append(Player(**{"name":"Arnaud","id":3,"color":(255,255,0)}))
        for i in range(1):
            self.bots.append(Bot(self.players[i],None))
        self.bots.append(CleverBot(self.players[1],None))
        

        kwargs = {"players":self.players}
        self.cm = CoreManager(**kwargs)
        for bot in self.bots:
            bot.cm = self.cm
        

    """def Call(self,name,**kwargs):
        act = Action(name,**kwargs)
        self.cm.SetAction(act)"""
    def Call(self,act):
        self.cm.SetAction(act)

    def Run(self):
        for bot in self.bots:
            botAct = bot.GetAction()
            for act in botAct:
                self.cm.SetAction(act)
                act.print()
        self.cm.Run()

    def print(self):
        self.cm.print()



