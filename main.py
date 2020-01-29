from building import Building
import config
import pygame
import csv
import numpy as np
import matplotlib.pyplot as plt

DONE     = False
TIME     = 0
SECONDS  = 0

config.menu()
Base = Building(config.FLOORNUMBER, config.ELEVATORNUMBER)

def resize():
    old_surface_saved = config.SCREEN
    old_size = config.SIZE
    config.SCREEN = config.pygame.display.set_mode((event.w, event.h), config.pygame.RESIZABLE)
    config.SIZE = [event.w, event.h]
    while(config.SIZE[1] % 100 != 0):
        config.SIZE = [config.SIZE[0], int(config.SIZE[1] - 1)]
    config.FLOORHEIGHT = config.SIZE[1] / config.FLOORNUMBER
    Base.resize(old_size)
    config.SCREEN.blit(old_surface_saved, (0,0))
    del old_surface_saved

while not DONE:
    TICK = config.CLOCK.tick(config.FPS)
    if config.ALGORITHM < 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                DONE = True
            if event.type == pygame.VIDEORESIZE:
                resize()
        Base.simulate(TICK, config.ALGORITHM)
    else:
        Base.simulate(TICK, config.ALGORITHM)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                DONE = True
            if event.type == pygame.VIDEORESIZE:
                resize()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                POSITION = pygame.mouse.get_pos()
                for i in Base.getFloors():
                    for j in i:
                        if j.getRect().getRectangle().collidepoint(POSITION) and j.getElevator().getStatus() == ["IDLE"] and j.getFloorNumber() != j.getElevator().getCurrentFloor():
                            j.getElevator().setStopList([j.getFloorNumber()])
                            if j.getElevator().getCurrentFloor() < j.getFloorNumber(): j.getElevator().setStatus(["UP"])
                            else: j.getElevator().setStatus(["DOWN"])
    TIME += TICK
    if TIME > 1000:
        TIME = 0
        SECONDS += 1
        if SECONDS in config.TIMEPASSENGERPAIRS:
            Base.addPassenger(config.TIMEPASSENGERPAIRS[SECONDS])
            del config.TIMEPASSENGERPAIRS[SECONDS]

def saveToExcel():
    with open('test.csv', 'w', newline='') as csvfile:
        fieldnames = ['Start', 'Destination', 'Wait', 'Finish', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for i in Base.Passengers:
            writer.writerow({'Start': i.getStartFloor(), 'Destination': i.getDestinationFloor(), 'Wait': int(i.getWaitTime() / 1000), 'Finish': int(i.getFinishTime() / 1000), 'Status': i.getStatus()})

def statistics():
    sumDistance=0
    for i in Base.getElevators():
        sumDistance+=i.getSumDistance()
    maxWait=0
    finishSum=0
    finishAverage=0
    for i in Base.Passengers:
        finishSum+=int(i.getFinishTime() / 1000)
        if int(i.getWaitTime() / 1000)>maxWait:
            maxWait=int(i.getWaitTime() / 1000)
    if(len(Base.Passengers)>0):
        finishAverage=finishSum/len(Base.Passengers)

    plt.title('Statistics')
    fig = plt.gcf()
    fig.canvas.set_window_title('Elevator Simulator')
    bars = ['Sumdistance by elevators', 'Avg WaitTime', 'Max WaitTime']
    datas = [sumDistance,finishAverage,maxWait]
    y_pos = np.arange(len(bars))
    plt.barh(y_pos,datas)
    plt.yticks(y_pos, bars)
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    plt.show()
"""
    ax.barh(y_pos, performance, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Performance')
    ax.set_title('How fast do you want to go today?')

    plt.show()
"""
saveToExcel()
config.pygame.quit()
statistics()
