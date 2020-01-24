import building
import config
import pygame
import csv
import tkinter as tk

DONE = False

Base = building.Building(config.FLOORNUMBER, config.ELEVATORNUMBER)
Base.addPassenger(config.PASSENGERNUMBER)

root = tk.Tk()
tk.Label(root, text = "Emeletek szama").grid(row = 0, sticky = tk.W)
tk.Label(root, text = "Liftek szama").grid(row = 1, sticky = tk.W)
tk.Label(root, text = "Utasok szama").grid(row = 2, sticky = tk.W)
tk.Label(root, text = "Random seed").grid(row = 3, sticky = tk.W)

EmeletSzam = tk.Entry(root)
LiftSzam = tk.Entry(root)
UtasSzam = tk.Entry(root)
RandomSeed = tk.Entry(root)


EmeletSzam.grid(row = 0, column = 1)
LiftSzam.grid(row = 1, column = 1)
UtasSzam.grid(row = 3, column = 1)
RandomSeed.grid(row = 2, column = 1)

def getInput():

    a = EmeletSzam.get()
    b = LiftSzam.get()
    c = UtasSzam.get()
    d = RandomSeed.get()
    e = v.get()
    root.destroy()

    global params
    params = [a,b,c,d,e]

v = tk.IntVar()
v.set(0)  # initializing the choice, i.e. Python

choices = [
    ("Algoritmus 1"),
    ("Algoritmus 2"),
    ("Algoritmus 3"),
    ("Manualis"),
]

def ShowChoice():
    print(v.get())

tk.Label(root, 
         text="""Liftet vezerlo algoritmus kivalasztasa:""",
         justify = tk.Left,
         padx = 20).grid(row = 4, sticky = tk.W)

for val, choices in enumerate(choices):
    tk.Radiobutton(root, 
                  text=choices,
                  padx = 20, 
                  variable=v, 
                  command=ShowChoice,
                  value=val).grid(row = 5+val, sticky = tk.W)



tk.Button(root, text = "Submit",
           command = getInput).grid(row = 10, sticky = tk.W)





root.mainloop()
print(params)


while not DONE:
    Base.simulate(config.CLOCK.tick(config.FPS))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            DONE = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            POSITION = pygame.mouse.get_pos()
            for i in Base.getFloors():
                for j in i:
                    if j.getRect().getRectangle().collidepoint(POSITION) and j.getElevator().getStatus() == ["IDLE"] and j.getFloorNumber() != j.getElevator().getCurrentFloor():
                        print("clicked floor: " + str(j.getFloorNumber()))
                        j.getElevator().setStopList([j.getFloorNumber()])
                        if j.getElevator().getCurrentFloor() < j.getFloorNumber(): j.getElevator().setStatus(["UP"])
                        else: j.getElevator().setStatus(["DOWN"])

with open('test.csv', 'w', newline='') as csvfile:
    fieldnames = ['Start', 'Destination', 'Wait', 'Finish']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    for i in Base.Passengers:
        writer.writerow({'Start': i.getStartFloor(), 'Destination': i.getDestinationFloor(), 'Wait': int(i.getWaitTime() / 1000), 'Finish': int(i.getFinishTime() / 1000)})


