import elevator
import passenger
import floor
import config
import random

class Building:
    def __init__(self, FloorNumber, ElevatorNumber):
        self.FloorNumber        = FloorNumber
        self.ElevatorNumber     = ElevatorNumber
        self.Elevators          = []
        self.Passengers         = []
        self.Floors             = []
        self.Lines              = []
        for i in range(10):
            print(config.random.randint(1, 20))
        self.addPassenger(config.BASEPASSENGERS)
        for i in range(ElevatorNumber):
            self.Elevators.append(elevator.Elevator(i))
            self.Floors.append([])
            [self.Floors[i].append(floor.Floor(self.Elevators[-1], j, config.FLOORHEIGHT)) for j in range(FloorNumber)]
        [self.Lines.append([(0, i * config.FLOORHEIGHT), (config.SIZE[0], i * config.FLOORHEIGHT)]) for i in range(FloorNumber)]
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
        [i.simulate_elevator(self.Floors[i.getID()], self.Passengers) for i in self.Elevators]
        self.draw()
