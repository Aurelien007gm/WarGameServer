class Log:

    def __init__(self):
        self.round = 1
        self.log = {0 : ["Game initialized"]}
        self.current_log = []
        self.info = {0 : ["Game initalized"]}
        self.current_info = []

    def Log(self,message):
        self.current_log.append(message)

    def Info(self,message):
        self.current_info.append(message)

    def CloseRound(self):
        self.log[self.round] = self.current_log
        self.info[self.round] = self.current_info
        self.round += 1
        self.current_log = []
        self.current_info = []

    def ToJson(self):
        #export log from previous round
        log = self.log[self.round-1]
        info = self.info[self.round-1]

        res = {"log":log,"info":info}
        return(res)
