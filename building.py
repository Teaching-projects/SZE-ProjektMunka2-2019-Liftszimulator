import random
import elevator
import passenger
import floor
import config
import rectangle

class Building:
    def __init__(self, FloorNumber, ElevatorNumber):
        self.FloorNumber        = FloorNumber
        self.ElevatorNumber     = ElevatorNumber
        self.Elevators          = []
        self.Passengers         = []
        self.Floors             = []
        self.Lines              = []
        for i in range(ElevatorNumber):
            self.Elevators.append(elevator.Elevator(i, config.FLOORHEIGHT))
            self.Floors.append([])
            [self.Floors[i].append(floor.Floor(self.Elevators[-1], j, config.FLOORHEIGHT)) for j in range(FloorNumber)]
        [self.Lines.append([(100, i * config.FLOORHEIGHT), ((config.FLOORWIDTH - 1) + self.ElevatorNumber * config.FLOORDISTANCE, i * config.FLOORHEIGHT)]) for i in range(FloorNumber)]
    def resize(self, oldsize):
        self.Lines.clear()
        [self.Lines.append([(100, i * config.FLOORHEIGHT), ((config.FLOORWIDTH - 1) + self.ElevatorNumber * config.FLOORDISTANCE, i * config.FLOORHEIGHT)]) for i in range(self.FloorNumber)]
        for elevator in self.Elevators:
            elevatorRect = rectangle.Rectangle(100 + config.FLOORDISTANCE * elevator.getID(), config.SIZE[1] / (oldsize[1] / elevator.getRect().getY()), config.FLOORWIDTH, config.FLOORHEIGHT, True)
            elevator.setRect(elevatorRect)
            for floorlist in self.Floors:
                for floor in floorlist:
                    floorRect = rectangle.Rectangle(100 + config.FLOORDISTANCE * floor.getElevator().getID(), (config.FLOORNUMBER - floor.getFloorNumber() - 1) * config.FLOORHEIGHT, config.FLOORWIDTH, config.FLOORHEIGHT, True)
                    floor.setRect(floorRect)
    def getFloors(self):        return self.Floors
    def getElevators(self):     return self.Elevators
    def getPassengers(self):    return self.Passengers
    def addPassenger(self, Passengernumber):    [self.Passengers.append(passenger.Passenger((random.sample((range(self.FloorNumber - 1)), 2)))) for i in range(Passengernumber)]
    def simulate_passengers(self, Time):         [i.increaseTime(Time) for i in self.Passengers]
    def draw(self):
        config.SCREEN.fill(config.WHITE)
        [config.pygame.draw.rect(config.SCREEN, config.RED,   i.getRect().getRectangle()) for j in range(self.ElevatorNumber) for i in self.Floors[j]]
        [config.pygame.draw.line(config.SCREEN, config.BLUE,  i[0], i[1], 1) for i in self.Lines]
        [config.pygame.draw.rect(config.SCREEN, config.BLACK, i.getRect().getRectangle()) for i in self.Elevators]
        [i.drawInfo() for i in self.Elevators]
        config.pygame.display.update()
    
    def simulate(self, Time):
        self.simulate_passengers(Time)
        stop=1
        upPassengers = []
        downPassengers = []
        [upPassengers.append(passenger) for passenger in self.Passengers if passenger.getDestinationFloor()>passenger.getStartFloor()]
        [downPassengers.append(passenger) for passenger in self.Passengers if passenger.getDestinationFloor()<passenger.getStartFloor()]
        for i in range(config.ELEVATORNUMBER):
            if self.Elevators[i].getTime() > 0.0:
                self.Elevators[i].setStatus(["WAITING: " + str(self.Elevators[i].getTime())])
                self.Elevators[i].setTime(self.Elevators[i].getTime() - Time)
                if self.Elevators[i].getTime() <= 0.0:
                    self.Elevators[i].setTime(0.0)
                    if self.Elevators[i].getStopList():
                        if self.Elevators[i].getStopList()[0] > self.Elevators[i].getCurrentFloor(): self.Elevators[i].setStatus(["UP"])
                        else:                                                      self.Elevators[i].setStatus(["DOWN"])
                    else: self.Elevators[i].setStatus(["IDLE"])



            if i<int(config.ELEVATORNUMBER/2):
                for passenger in upPassengers:
                    if len(self.Elevators[i].getStopList())<stop:
                        if passenger.getStatus()=="WAITING":
                            if passenger.getStartFloor()==0:
                                self.Elevators[i].addPassenger(passenger)
                                passenger.setStatus("INLIFT")
                            else:
                                self.Elevators[i].addToStopList(passenger.getStartFloor())
                                passenger.setStatus("INPROGRESS")  
                if self.Elevators[i].getStopList():
                    if self.Elevators[i].getStatus()==(["UP"]):
                        self.Elevators[i].move(-1)
                        for floor in self.Floors[self.Elevators[i].getID()]:
                            if floor.getRect().getRectangle().contains(self.Elevators[i].getRect().getRectangle()):
                                self.Elevators[i].setCurrentFloor(floor.getFloorNumber())
                        if self.Elevators[i].getCurrentFloor() in self.Elevators[i].getStopList():
                            self.Elevators[i].setStatus(["IDLE"])
                            self.Elevators[i].setTime(3000)
                            self.Elevators[i].getStopList().remove(self.Elevators[i].getCurrentFloor())
                            for passenger in self.Elevators[i].getPassengers():
                                if passenger.getDestinationFloor()==self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].deletePassenger(passenger)
                            for passenger in upPassengers:
                                if passenger.getStatus() in ["INPROGRESS", "WAITING"] and self.Elevators[i].getCurrentPassengers() < self.Elevators[i].getMaxPassengers() and passenger.getStartFloor() == self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].addPassenger(passenger)
                            for passenger in self.Elevators[i].getPassengers():
                                self.Elevators[i].addToStopList(passenger.getDestinationFloor())
                    if self.Elevators[i].getStatus()==(["DOWN"]):
                        self.Elevators[i].move(1)
                        for floor in self.Floors[self.Elevators[i].getID()]:
                            if floor.getRect().getRectangle().contains(self.Elevators[i].getRect().getRectangle()):
                                self.Elevators[i].setCurrentFloor(floor.getFloorNumber())
                        if self.Elevators[i].getStopList() and self.Elevators[i].getCurrentFloor() in self.Elevators[i].getStopList():
                            self.Elevators[i].setStatus(["IDLE"])
                            self.Elevators[i].setTime(3000)
                            self.Elevators[i].getStopList().remove(self.Elevators[i].getCurrentFloor())
                            for passenger in self.Elevators[i].getPassengers():
                                if passenger.getDestinationFloor()==self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].deletePassenger(passenger)
                            for passenger in upPassengers:
                                if passenger.getStatus() in ["INPROGRESS", "WAITING"] and self.Elevators[i].getCurrentPassengers() < self.Elevators[i].getMaxPassengers() and passenger.getStartFloor() == self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].addPassenger(passenger)
                            for passenger in self.Elevators[i].getPassengers():
                                self.Elevators[i].addToStopList(passenger.getDestinationFloor())
                else:
                    if self.Elevators[i].getCurrentFloor()!=0 and self.Elevators[i].getStatus()==(["IDLE"]) and len(self.Elevators[i].getStopList())==0: 
                        self.Elevators[i].addToStopList(0)
                                 
            
            else:
                for passenger in downPassengers:
                    if len(self.Elevators[i].getStopList())<stop:
                        if passenger.getStatus()=="WAITING":
                            if passenger.getStartFloor()==0:
                                self.Elevators[i].addPassenger(passenger)
                                passenger.setStatus("INLIFT")
                            else:
                                self.Elevators[i].addToStopList(passenger.getStartFloor())
                                passenger.setStatus("INPROGRESS")  
                if self.Elevators[i].getStopList():
                    if self.Elevators[i].getStatus()==(["UP"]):
                        self.Elevators[i].move(-1)
                        for floor in self.Floors[self.Elevators[i].getID()]:
                            if floor.getRect().getRectangle().contains(self.Elevators[i].getRect().getRectangle()):
                                self.Elevators[i].setCurrentFloor(floor.getFloorNumber())
                        if self.Elevators[i].getStopList() and self.Elevators[i].getCurrentFloor() in self.Elevators[i].getStopList():
                            self.Elevators[i].setStatus(["IDLE"])
                            self.Elevators[i].setTime(3000)
                            self.Elevators[i].getStopList().remove(self.Elevators[i].getCurrentFloor())
                            for passenger in self.Elevators[i].getPassengers():
                                if passenger.getDestinationFloor()==self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].deletePassenger(passenger)
                            for passenger in downPassengers:
                                if passenger.getStatus() in ["INPROGRESS", "WAITING"] and self.Elevators[i].getCurrentPassengers() < self.Elevators[i].getMaxPassengers() and passenger.getStartFloor() == self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].addPassenger(passenger)
                            for passenger in self.Elevators[i].getPassengers():
                                self.Elevators[i].addToStopList(passenger.getDestinationFloor())
                    if self.Elevators[i].getStatus()==(["DOWN"]):
                        self.Elevators[i].move(1)
                        for floor in self.Floors[self.Elevators[i].getID()]:
                            if floor.getRect().getRectangle().contains(self.Elevators[i].getRect().getRectangle()):
                                self.Elevators[i].setCurrentFloor(floor.getFloorNumber())
                        if self.Elevators[i].getStopList() and self.Elevators[i].getCurrentFloor() in self.Elevators[i].getStopList():
                            self.Elevators[i].setStatus(["IDLE"])
                            self.Elevators[i].setTime(3000)
                            self.Elevators[i].getStopList().remove(self.Elevators[i].getCurrentFloor())
                            for passenger in self.Elevators[i].getPassengers():
                                if passenger.getDestinationFloor()==self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].deletePassenger(passenger)
                            for passenger in downPassengers:
                                if passenger.getStatus() in ["INPROGRESS", "WAITING"] and self.Elevators[i].getCurrentPassengers() < self.Elevators[i].getMaxPassengers() and passenger.getStartFloor() == self.Elevators[i].getCurrentFloor():
                                    self.Elevators[i].addPassenger(passenger)
                            for passenger in self.Elevators[i].getPassengers():
                                self.Elevators[i].addToStopList(passenger.getDestinationFloor())
                elif self.Elevators[i].getCurrentFloor()!=config.FLOORNUMBER-1 and self.Elevators[i].getStatus()==(["IDLE"]) and len(self.Elevators[i].getStopList())==0: 
                     self.Elevators[i].addToStopList(config.FLOORNUMBER-1)
            self.draw()



       