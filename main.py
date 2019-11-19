import building
import config
import pygame

DONE = False

Base = building.Building(config.FLOORNUMBER, config.ELEVATORNUMBER)
Base.addPassenger(config.PASSENGERNUMBER)

while not DONE:
    for event in pygame.event.get():
        pass
    Base.Simulate(config.CLOCK.tick(config.FPS))

