class Log:

    def __init__(self):
        self.round = 1
        self.log = {0 : ["Game initialized"]}
        self.current_log = []

    def Log(self,message):
        self.current_log.append(message)

    def CloseRound(self):
        self.log[self.round] = self.current_log
        self.round += 1
        self.current_log

    def ToJson(self):
        #export log from previous round
        log = self.log[self.round-1]
        return(log)
