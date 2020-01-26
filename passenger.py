class Passenger:
    def __init__(self, Start_Destination):       
        self.StartFloor         = Start_Destination[0]
        self.DestinationFloor   = Start_Destination[1]
        self.WaitTime           = 0.0
        self.FinishTime         = 0.0
        self.Status             = "WAITING" #ARRIVED INLIFT
    def getStatus(self):                    return self.Status
    def setStatus(self, Status):            self.Status = Status
    def getStartFloor(self):                return self.StartFloor
    def getDestinationFloor(self):          return self.DestinationFloor
    def getWaitTime(self):                  return self.WaitTime
    def getFinishTime(self):                return self.FinishTime
    def increaseTime(self, Time):
        if self.Status in ["WAITING", "INPROGRESS"]:
            self.WaitTime += Time
            self.FinishTime += Time
        elif self.Status == "INLIFT":
            self.FinishTime += Time
