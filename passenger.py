class Passenger:
    def __init__(self, Start_Destination):       
        self.StartFloor         = Start_Destination[0]
        self.DestinationFloor   = Start_Destination[1]
        self.WaitTime           = 0.0
        self.FinishTime         = 0.0
        self.Status             = "WAITING"
    def getStatus(self):                    return self.Status
    def setStatus(self, Status):            self.Status = Status
    def getStartFloor(self):                return self.StartFloor
    def getDestinationFloor(self):          return self.DestinationFloor
    def getWaitTime(self):                  return self.WaitTime
    def getFinishTime(self):                return self.FinishTime
    def increaseWaitTime(self, Time):       self.WaitTime    += Time
    def increaseFinishTime(self, Time):     self.FinishTime  += Time