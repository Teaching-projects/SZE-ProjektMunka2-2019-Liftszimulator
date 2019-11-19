import rectangle
import config

class Elevator:
    def __init__(self, Number):
        self.ID                 = Number
        self.CurrentPassengers  = 0
        self.maxPassenger       = 8
        self.CurrentFloor       = 0
        self.StopList           = []
        self.Status             = ["IDLE"]
        self.Rect               = rectangle.Rectangle(100 + 100 * Number, config.SIZE[1] - config.FLOORHEIGHT, 90, config.FLOORHEIGHT, True)
        self.Passengers         = []
        self.Data               = dict()
        self.renderedText       = []
        self.refreshData()
        self.renderText()
    def getID(self):                        return self.ID
    def getCurrentPassengers(self):         return self.CurrentPassengers
    def getCurrentFloor(self):              return self.CurrentFloor
    def setCurrentFloor(self, Number):      self.CurrentFloor = Number
    def getStopList(self):                  return self.StopList
    def getStatus(self):                    return self.Status
    def setStatus(self, Status):            self.Status = Status
    def getRect(self):                      return self.Rect
    def getPassengers(self):                return self.Passengers
    def move(self, y):                      self.Rect.move(y)
    def deletePassenger(self, Passenger):   self.Passengers.remove(Passenger)
    def setCurrentPassengers(self):         self.CurrentPassengers = len(self.Passengers)
    def refreshData(self):
        self.Data.clear()
        self.Data["StopList"]           = self.StopList
        self.Data["Status"]             = self.Status
        self.Data["CurrentPassengers"]  = self.CurrentPassengers
    def getData(self):                      return self.Data
    def renderText(self):
            self.renderedText.clear()
            messages = [self.getStatus()[0], "Stoplist: ", "Utasszam: "]
            temp = []
            [temp.append(i.getDestinationFloor()) for i in self.Passengers if i.getDestinationFloor not in temp]
            [messages[1].join(str(i) + " ") for i in temp]
            if len(self.getPassengers()) > 0: messages[2] += str(len(i.getPassengers()))
            [self.renderedText.append(config.SMALLFONT.render(i, True, (0, 0, 255))) for i in messages]
    def Draw(self):
        if self.Data["StopList"] != self.StopList or self.Data["Status"] != self.Status or self.Data["CurrentPassengers"] != self.CurrentPassengers:
            self.renderText()
        distance = 0
        for i in self.renderedText:
            config.SCREEN.blit(i, config.pygame.Rect(self.getRect().getRectangle().move(0, distance)))
            distance += 20


