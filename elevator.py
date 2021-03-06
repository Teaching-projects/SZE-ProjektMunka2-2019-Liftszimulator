from rectangle import Rectangle
import config
from decimal import Decimal

class Elevator:
    def __init__(self, Number, FloorHeight):
        self.ID                 = Number
        self.CurrentPassengers  = 0
        self.MaxPassenger       = 8
        self.CurrentFloor       = 0
        self.StopList           = []
        self.Status             = ["IDLE"]
        self.Rect               = Rectangle(100 + config.FLOORWIDTH * self.ID, config.SIZE[1] - FloorHeight, config.FLOORWIDTH, FloorHeight, True)
        self.Passengers         = []
        self.Data               = dict()
        self.RenderedText       = []
        self.SectorList         = []
        self.Time               = 0.0
        self.sumDistance        = 0
        self.renderText(0)
        #self.setSector()
    def getID(self):                        return self.ID
    def getCurrentPassengers(self):         return self.CurrentPassengers
    def getCurrentFloor(self):              return self.CurrentFloor
    def setCurrentFloor(self, Number):      self.CurrentFloor = Number
    def getStopList(self):                  return self.StopList
    def setStopList(self, StopList):        self.StopList = StopList
    def getStatus(self):                    return self.Status
    def setStatus(self, Status):            self.Status = Status
    def getRect(self):                      return self.Rect
    def setRect(self, Rect):                self.Rect = Rect
    def getPassengers(self):                return self.Passengers
    def getMaxPassengers(self):             return self.MaxPassenger
    def move(self, y):                      self.Rect.move(y)
    def getTime(self):                      return self.Time
    def setTime(self, Time):                self.Time = Time
    def sumDistanceIncrease(self):          self.sumDistance+=1
    def getSumDistance(self):               return self.sumDistance
    def setSector(self, sectorList):        self.SectorList = sectorList
    def deletePassenger(self, Passenger):
        self.Passengers.remove(Passenger)
        self.setCurrentPassengers()
        Passenger.setStatus("ARRIVED")
    def addPassenger(self, Passenger):
        self.Passengers.append(Passenger)
        self.setCurrentPassengers()
        Passenger.setStatus("INLIFT")
    def setCurrentPassengers(self):         self.CurrentPassengers = len(self.Passengers)
    def checkPassengers(self, Passengers):
        for i in self.Passengers:
            if i.getDestinationFloor() == self.CurrentFloor:
                self.deletePassenger(i)
        for i in Passengers:
            if i.getStartFloor() == self.CurrentFloor and self.CurrentPassengers < self.MaxPassenger and i.getStatus() == "WAITING":
                self.addPassenger(i)
    def refreshData(self):
        self.Data.clear()
        self.Data["CurrentFloor"]       = self.CurrentFloor
        self.Data["StopList"]           = self.StopList
        self.Data["Status"]             = self.Status
        self.Data["CurrentPassengers"]  = self.CurrentPassengers
    def getData(self):                      return self.Data
    def renderText(self, Algorithm):
        self.refreshData()
        self.RenderedText.clear()
        messages = [str(self.getCurrentFloor()) + " " + self.getStatus()[0], "", "Passengers: "]
        temp = []
        if Algorithm != 3:
            [temp.append(str(i)) for i in self.StopList]
        else:
            [temp.append(str(passenger.getDestinationFloor())) for passenger in self.Passengers if str(passenger.getDestinationFloor()) not in temp]
        messages[1] += " ".join(temp)
        messages[2] += str(len(self.Passengers))
        [self.RenderedText.append(config.SMALLFONT.render(i, True, config.BLUE)) for i in messages]
    def drawInfo(self, Algorithm):
        if self.Data["CurrentFloor"] != self.CurrentFloor or self.Data["StopList"] != self.StopList or self.Data["Status"] != self.Status or self.Data["CurrentPassengers"] != self.CurrentPassengers:
            self.renderText(Algorithm)
        distance = 0
        for i in self.RenderedText:
            config.SCREEN.blit(i, config.pygame.Rect(self.getRect().getRectangle().move(0, distance)))
            distance += 15
    def addToStopList(self, floorNumber):
        if floorNumber not in self.StopList and floorNumber != self.CurrentFloor:
            self.StopList.append(floorNumber)
            if self.Status == ["IDLE"] and self.StopList[0] > self.CurrentFloor:    self.Status = ["UP"]
            elif self.Status == ["IDLE"]:                                           self.Status = ["DOWN"]
        LessThenCurrentFloor, MoreThenCurrentFloor = [], []
        for i in self.StopList:
            if i < self.CurrentFloor:   LessThenCurrentFloor.append(i)
            else:                       MoreThenCurrentFloor.append(i)
        if self.Status == ["DOWN"]: self.StopList = sorted(LessThenCurrentFloor, reverse = True)    + sorted(MoreThenCurrentFloor)
        elif self.Status == ["UP"]: self.StopList = sorted(MoreThenCurrentFloor)                    + sorted(LessThenCurrentFloor, reverse = True)
    def simulateManualControlling(self, Floor, Passengers):
        if self.Status == ["IDLE"]:
            self.checkPassengers(Passengers)
        elif self.Status == ["UP"]:
            self.move(-1)
            for floor in Floor:
                if floor.getRect().getRectangle().contains(self.getRect().getRectangle()):
                    if self.CurrentFloor!=floor.getFloorNumber():
                        self.sumDistance+=1
                        self.CurrentFloor = floor.getFloorNumber()
            if Floor[config.FLOORNUMBER - 1 - self.StopList[0]].getRect().getRectangle().contains(self.getRect().getRectangle()):
                self.setStatus(["IDLE"])
                self.StopList.pop(0)
        elif self.Status == ["DOWN"]:
            self.move(1)
            for floor in Floor:
                if floor.getRect().getRectangle().contains(self.getRect().getRectangle()):
                    if self.CurrentFloor!=floor.getFloorNumber():
                        self.sumDistance+=1
                        self.CurrentFloor = floor.getFloorNumber()
            if Floor[config.FLOORNUMBER - 1 - self.StopList[0]].getRect().getRectangle().contains(self.getRect().getRectangle()):
                self.setStatus(["IDLE"])
                self.StopList.pop(0)
    def simulateSectorAlgorithm(self, Floor, Passengers, Time):
        if self.Time > 0.0:
            self.Time -= Time
            self.Status = ["WAIT: " + str(self.Time)]
            if self.Time <= 0.0:
                self.Status = ["IDLE"]
                self.Time = 0.0
        if self.Status == ["IDLE"]:
            for passenger in self.Passengers: # Ha a passengerek közül valakinek ez a célállomása akkor kiszáll
                if passenger.getDestinationFloor() == self.CurrentFloor:        self.deletePassenger(passenger)
            floorsWithWaiters = []
            for passenger in Passengers:
                if passenger.getStatus() == "WAITING" and passenger.getStartFloor() in self.SectorList and passenger.getStartFloor() not in floorsWithWaiters:
                    floorsWithWaiters.append(passenger.getStartFloor())
            if self.CurrentFloor in self.SectorList: # Ha a lift olyan szinten van ami a szektorába tartozik akkor felevesz annyi embert amennyit tud
                for passenger in Passengers:
                    if passenger.getStatus() == "WAITING" and passenger.getStartFloor() == self.CurrentFloor:
                        self.addPassenger(passenger)
                        if self.Status == ["IDLE"] and not self.StopList: # az első beszálló célja felé(UP vagy DOWN beállítja a lift státuszát)
                            if self.CurrentFloor - passenger.getDestinationFloor() > 0:     self.Status = ["DOWN"]
                            else:                                                           self.Status = ["UP"]
                        if self.CurrentPassengers >= self.MaxPassenger: break
            else: # ha nem olyan szinte vagyunk ami a szektorunkba tartozik akkor a legközelibb szektorszintől kezdve a legtávolabbiig beállítjuk a stoplistát, így megáll az összes szektorszinten
                if self.CurrentFloor < min(self.SectorList):
                    for i in self.SectorList:
                        if i not in self.StopList and i in floorsWithWaiters:
                            self.StopList.append(i)
                else:
                    if self.CurrentFloor > max(self.SectorList):
                        for i in sorted(self.SectorList, reverse = True):
                            if i not in self.StopList and i in floorsWithWaiters:
                                self.StopList.append(i)
            for i in self.Passengers:# A felvett emberek destinationfloor ját berakjuk a stoplistába
                if i.getDestinationFloor() not in self.StopList:
                    self.StopList.append(i.getDestinationFloor())
            if self.Status == ["IDLE"] and self.StopList: # Ha nem állítódott be irány akkor azt most állítjuk be
                for passenger in self.Passengers:
                    if passenger.getDestinationFloor() == self.CurrentFloor:        self.deletePassenger(passenger)
                if self.CurrentFloor - self.StopList[0] > 0:    self.Status = ["DOWN"]
                else:                                           self.Status = ["UP"]
            if self.StopList and self.Status == ["DOWN"]:
                if min(self.StopList) < min(self.SectorList):
                    for i in self.SectorList:
                        if i < self.CurrentFloor and i not in self.StopList and i in floorsWithWaiters:
                            self.StopList.append(i)
            elif self.StopList and self.Status == ["UP"]:
                if max(self.StopList) < max(self.SectorList):
                    for i in self.SectorList:
                        if i < self.CurrentFloor and i not in self.StopList and i in floorsWithWaiters:
                            self.StopList.append(i)
            LessThenCurrentFloor, MoreThenCurrentFloor = [], [] # Irány szerint sorba rendezzük a listát pl: currentfloor: 3 és felfele megyünk stoplist [1, 2, 4, 5,] -> [4, 5, 2, 1]
            for i in self.StopList:
                if i < self.CurrentFloor:   LessThenCurrentFloor.append(i)
                else:                       MoreThenCurrentFloor.append(i)
            if self.Status == ["DOWN"]: self.StopList = sorted(LessThenCurrentFloor, reverse = True)    + sorted(MoreThenCurrentFloor)
            elif self.Status == ["UP"]: self.StopList = sorted(MoreThenCurrentFloor)                    + sorted(LessThenCurrentFloor, reverse = True)
        if self.Status == ["UP"]:
            self.move(-1)
            for floor in Floor:
                if floor.getRect().getRectangle().contains(self.getRect().getRectangle()):
                    if self.CurrentFloor!=floor.getFloorNumber():
                        self.sumDistance+=1
                        self.CurrentFloor = floor.getFloorNumber()
            if self.CurrentFloor == self.StopList[0]:
                for passenger in self.Passengers: # Ha a passengerek közül valakinek ez a célállomása akkor kiszáll
                    if passenger.getDestinationFloor() == self.CurrentFloor:        self.deletePassenger(passenger)
                self.setStatus(["WAIT: 3000"])
                self.Time = 3000
                self.StopList.pop(0)
        if self.Status == ["DOWN"]:
            self.move(1)
            for floor in Floor:
                if floor.getRect().getRectangle().contains(self.getRect().getRectangle()):
                    if self.CurrentFloor!=floor.getFloorNumber():
                        self.sumDistance+=1
                        self.CurrentFloor = floor.getFloorNumber()
            if self.CurrentFloor == self.StopList[0]:
                for passenger in self.Passengers: # Ha a passengerek közül valakinek ez a célállomása akkor kiszáll
                    if passenger.getDestinationFloor() == self.CurrentFloor:        self.deletePassenger(passenger)
                self.setStatus(["WAIT"])
                self.Time = 3000
                self.StopList.pop(0)
