from elevator import Elevator
from passenger import Passenger
from floor import Floor
import config
import random
from rectangle import Rectangle


class Building:
    def __init__(self, FloorNumber, ElevatorNumber):
        self.FloorNumber        = FloorNumber
        self.ElevatorNumber     = ElevatorNumber
        self.Elevators          = []
        self.Passengers         = []
        self.Floors             = []
        self.Lines              = []
        self.RenderedText       = []
        self.FloorNumberRects   = []
        self.PressedButtonsRect = []
        self.addPassenger(config.BASEPASSENGERS)
        for i in range(ElevatorNumber):
            self.Elevators.append(Elevator(i, config.FLOORHEIGHT))
            self.Floors.append([])
            [self.Floors[i].append(Floor(self.Elevators[-1], j, config.FLOORHEIGHT)) for j in range(FloorNumber)]
        [self.Lines.append([(100, i * config.FLOORHEIGHT), ((config.FLOORWIDTH - 1) + self.ElevatorNumber * config.FLOORDISTANCE, i * config.FLOORHEIGHT)]) for i in range(FloorNumber)]
        [self.RenderedText.append(config.BIGFONT.render(str(i), True, config.BLUE)) for i in range(FloorNumber)]
        self.resizeFloorNumbers()
        self.resizePressedButtons()
    def resize(self, oldsize):
        self.Lines.clear()
        [self.Lines.append([(100, i * config.FLOORHEIGHT), ((config.FLOORWIDTH - 1) + self.ElevatorNumber * config.FLOORDISTANCE, i * config.FLOORHEIGHT)]) for i in range(self.FloorNumber)]
        for elevator in self.Elevators:
            elevatorRect = Rectangle(100 + config.FLOORDISTANCE * elevator.getID(), config.SIZE[1] / (oldsize[1] / elevator.getRect().getY()), config.FLOORWIDTH, config.FLOORHEIGHT, True)
            elevator.setRect(elevatorRect)
            for floorlist in self.Floors:
                for floor in floorlist:
                    floorRect = Rectangle(100 + config.FLOORDISTANCE * floor.getElevator().getID(), (config.FLOORNUMBER - floor.getFloorNumber() - 1) * config.FLOORHEIGHT, config.FLOORWIDTH, config.FLOORHEIGHT, True)
                    floor.setRect(floorRect)
        self.resizeFloorNumbers()
        self.resizePressedButtons()
    def resizePressedButtons(self):
        self.PressedButtonsRect.clear()
        tempRectUp      = config.pygame.Rect(30, (config.FLOORNUMBER - 1) * config.FLOORHEIGHT,                          70, config.FLOORHEIGHT / 2)
        tempRectDown    = config.pygame.Rect(30, (config.FLOORNUMBER - 1) * config.FLOORHEIGHT + config.FLOORHEIGHT / 2 + 1, 70, config.FLOORHEIGHT / 2)
        for floor in range(self.FloorNumber):
            self.PressedButtonsRect.append([tempRectUp, tempRectDown])
            tempRectUp = tempRectUp.move(0, -1 * config.FLOORHEIGHT)
            tempRectDown = tempRectDown.move(0, -1 * config.FLOORHEIGHT)
        for floor in self.PressedButtonsRect:
            config.pygame.draw.rect(config.SCREEN, config.RED, floor[0])
            config.pygame.draw.rect(config.SCREEN, config.BLUE, floor[1])
    def resizeFloorNumbers(self):
        self.FloorNumberRects.clear()
        tempRect = config.pygame.Rect(0, (config.FLOORNUMBER - 1) * config.FLOORHEIGHT + config.FLOORHEIGHT / 3, 30, config.FLOORHEIGHT)
        for text in self.RenderedText:
            self.FloorNumberRects.append(tempRect)
            config.SCREEN.blit(text, config.pygame.Rect(tempRect))
            tempRect = tempRect.move(0, -1 * config.FLOORHEIGHT)
    def drawFloorNumbers(self):     [config.SCREEN.blit(text, rect) for rect, text in zip(self.FloorNumberRects, self.RenderedText)]
    def drawPressedButtons(self):
        for floor in self.PressedButtonsRect:
            config.pygame.draw.rect(config.SCREEN, config.RED, floor[0])
            config.pygame.draw.rect(config.SCREEN, config.BLUE, floor[1])
    def getFloors(self):        return self.Floors
    def getElevators(self):     return self.Elevators
    def getPassengers(self):    return self.Passengers
    def addPassenger(self, Passengernumber):    [self.Passengers.append(Passenger((random.sample((range(self.FloorNumber - 1)), 2)))) for i in range(Passengernumber)]
    def simulatePassengers(self, Time):         [i.increaseTime(Time) for i in self.Passengers]
    def draw(self):
        config.SCREEN.fill(config.ORANGE)
        self.drawFloorNumbers()
        self.drawPressedButtons()
        [config.pygame.draw.rect(config.SCREEN, config.RED,   i.getRect().getRectangle()) for j in range(self.ElevatorNumber) for i in self.Floors[j]]
        [config.pygame.draw.line(config.SCREEN, config.GREEN,  i[0], i[1], 1) for i in self.Lines]
        [config.pygame.draw.rect(config.SCREEN, config.GRAY, i.getRect().getRectangle()) for i in self.Elevators]
        [i.drawInfo() for i in self.Elevators]
        config.pygame.display.update()
    def simulate(self, Time, Algorithm):
        self.simulatePassengers(Time)
        if Algorithm == 3:
            self.simulateNearestCar(Time)
        elif Algorithm == 2:
            [i.simulateSectorAlgorithm(self.Floors[i.getID()], self.Passengers, Time) for i in self.Elevators]
        elif Algorithm == 1:
            pass
        self.draw()
    def simulateNearestCar(self, Time):
        maxStop = 3
        inProgressFloors = set()
        [inProgressFloors.add(passenger.getStartFloor()) for passenger in self.Passengers if passenger.getStatus() == "INPROGRESS"]
        waitingPassengers = []
        [waitingPassengers.append(passenger) for passenger in self.Passengers if passenger.getStatus() == "WAITING"]
        for passenger in waitingPassengers:
            if passenger.getStartFloor() not in inProgressFloors:
                solutionValue = -1
                solutionElevator = self.Elevators[0]
                for elevator in self.Elevators:
                    if len(elevator.getStopList()) < maxStop:
                        distance = abs(passenger.getStartFloor() - elevator.getCurrentFloor())
                        passengerGoingUp = 0 < (passenger.getStartFloor() - elevator.getCurrentFloor())
                        solutionValueForThisElevator = 1
                        if elevator.getStatus() == ["IDLE"]:
                            solutionValueForThisElevator = config.FLOORNUMBER + 1 - distance
                        elif elevator.getStatus() == ["DOWN"]:
                            if passengerGoingUp:
                                solutionValueForThisElevator = 1
                            elif passenger.getDestinationFloor() in elevator.getStopList():
                                solutionValueForThisElevator = config.FLOORNUMBER + 2 - distance
                            else:
                                solutionValueForThisElevator = config.FLOORNUMBER + 1 - distance
                        elif elevator.getStatus() == ["UP"]:
                            if not passengerGoingUp:
                                solutionValueForThisElevator = 1
                            elif passenger.getDestinationFloor() in elevator.getStopList():
                                solutionValueForThisElevator = config.FLOORNUMBER + 2 - distance
                            else:
                                solutionValueForThisElevator = config.FLOORNUMBER + 1 - distance
                        if solutionValueForThisElevator > solutionValue:
                            solutionValue = solutionValueForThisElevator
                            solutionElevator = elevator
                if solutionValue > 0:
                    passenger.setStatus("INPROGRESS")
                    inProgressFloors.add(passenger.getStartFloor())
                    solutionElevator.addToStopList(passenger.getStartFloor())
        unitedStopLists = set()
        for elevator in self.Elevators:
            if elevator.getTime() > 0.0:
                elevator.setStatus(["WAITING: " + str(elevator.getTime())])
                elevator.setTime(elevator.getTime() - Time)
                if elevator.getTime() <= 0.0:
                    elevator.setTime(0.0)
                    if elevator.getStopList():
                        if elevator.getStopList()[0] > elevator.getCurrentFloor(): elevator.setStatus(["UP"])
                        else:                                                      elevator.setStatus(["DOWN"])
                    else: elevator.setStatus(["IDLE"])
            if elevator.getStatus() == ["UP"]:
                elevator.move(-1)
                for floor in self.Floors[elevator.getID()]:
                    if floor.getRect().getRectangle().contains(elevator.getRect().getRectangle()):
                        elevator.setCurrentFloor(floor.getFloorNumber())
                if elevator.getStopList() and elevator.getCurrentFloor() == elevator.getStopList()[0]:
                    elevator.setStatus(["IDLE"])
                    elevator.setTime(3000)
                    elevator.StopList.pop(0)
                    for passenger in elevator.getPassengers():
                        if passenger.getDestinationFloor() == elevator.getCurrentFloor():
                            elevator.deletePassenger(passenger)
                    for passenger in self.Passengers:
                        if passenger.getStatus() in ["INPROGRESS", "WAITING"] and elevator.getCurrentPassengers() < elevator.getMaxPassengers() and passenger.getStartFloor() == elevator.getCurrentFloor():
                            elevator.addPassenger(passenger)
                    for passenger in elevator.getPassengers():
                        elevator.addToStopList(passenger.getDestinationFloor())
            elif elevator.getStatus() == ["DOWN"]:
                elevator.move(1)
                for floor in self.Floors[elevator.getID()]:
                    if floor.getRect().getRectangle().contains(elevator.getRect().getRectangle()):
                        elevator.setCurrentFloor(floor.getFloorNumber())
                if elevator.getStopList() and elevator.getCurrentFloor() == elevator.getStopList()[0]:
                    elevator.setStatus(["IDLE"])
                    elevator.setTime(3000)
                    elevator.StopList.pop(0)
                    for passenger in elevator.getPassengers():
                        if passenger.getDestinationFloor() == elevator.getCurrentFloor():
                            elevator.deletePassenger(passenger)
                    for passenger in self.Passengers:
                        if passenger.getStatus() in ["INPROGRESS", "WAITING"] and elevator.getCurrentPassengers() < elevator.getMaxPassengers() and passenger.getStartFloor() == elevator.getCurrentFloor():
                            elevator.addPassenger(passenger)
                    for passenger in elevator.getPassengers():
                        elevator.addToStopList(passenger.getDestinationFloor())
            [unitedStopLists.add(stopListItem) for stopListItem in elevator.getStopList()]
        [passenger.setStatus("WAITING") for passenger in self.Passengers if passenger.getStatus() == "INPROGRESS" and passenger.getStartFloor() not in list(unitedStopLists)]
        self.draw()
