from coremanager import CoreManager
from bot import Bot, CleverBot
from action import Action
from player import Player

# Main instance of a game
class Game:
    def __init__(self, players_json):
        name = [p.get('name') for p in players_json]
        is_bot = [p.get('bot') for p in players_json]
        print(is_bot)
        self.players = []
        self.bots =[]
        self.players.append(Player(**{"name":name[0],"id":0,"color":(0,0,255),"isbot":is_bot[0]}))
        self.players.append(Player(**{"name":name[1],"id":1,"color":(0,255,0),"isbot":is_bot[1]}))
        self.players.append(Player(**{"name":name[2],"id":2,"color":(255,0,0),"isbot":is_bot[2]}))
        self.players.append(Player(**{"name":name[3],"id":3,"color":(255,255,0),"isbot":is_bot[3]}))
        for i in range(4):
            if is_bot[i]:
                self.bots.append(Bot(self.players[i],None))
        

        kwargs = {"players":self.players}
        self.cm = CoreManager(**kwargs)
        for bot in self.bots:
            bot.cm = self.cm
        self.round = 1
        

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
        print(f"Time for round {self.round}")
        print("Print all action on Run")
        for a in self.cm.actions:
            a.print()
        self.cm.Run()
        self.round += 1

    def print(self):
        self.cm.print()

    def ToJson(self):
        return(self.cm.ToJson())
    
    def StaticTerritoriesToJson(self):
        return(self.cm.StaticTerritoriesToJson())
    
    def Validate(self, p):
        run = self.cm.Validate(p)
        if(run):
            self.Run()



