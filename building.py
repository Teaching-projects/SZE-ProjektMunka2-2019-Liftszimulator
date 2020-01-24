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
        #[i.simulate_elevator(self.Floors[i.getID()], self.Passengers) for i in self.Elevators]
        [i.simulateSectorAlgorithm(self.Floors[i.getID()], self.Passengers, Time) for i in self.Elevators]
        self.draw()
