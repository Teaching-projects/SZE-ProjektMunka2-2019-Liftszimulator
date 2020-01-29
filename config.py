import pygame
import random
import tkinter as tk

pygame.init()
pygame.display.set_caption('Elevator simulator')

SIZE            = [1600, 900]
FLOORNUMBER     = 5
ELEVATORNUMBER  = 2
BASEPASSENGERS  = 0
PASSENGERNUMBER = 10
FPS             = 60
FLOORHEIGHT     = SIZE[1] / FLOORNUMBER
SEED            = random.randint(0, 2 ** 10)
ALGORITHM       = 3
TIMEINTERVALL   = 120
FLOORWIDTH      = 90
FLOORDISTANCE   = 100

CLOCK           = pygame.time.Clock()
SCREEN          = None
SMALLFONT       = pygame.font.SysFont(None, 16)
BIGFONT         = pygame.font.SysFont(None, 64)
TIMEPASSENGERPAIRS = dict()
PASSENGERPAIRS     = dict()


BLUE    = (69,  173, 168)
ORANGE  = (168, 167, 167)
GRAY    = (42,  54,  59)
RED     = (232, 74,  95)
GREEN   = (153, 184, 152)


def isInt(value):
    try:
        return float(str(value)).is_integer()
    except:
        return False

def menu():
    def getInput():
        global FLOORNUMBER
        global ELEVATORNUMBER
        global PASSENGERNUMBER
        global FLOORHEIGHT
        global SEED
        global TIMEINTERVALL
        global BASEPASSENGERS
        global ALGORITHM
        global TIMEPASSENGERPAIRS
        global SCREEN
        global PASSENGERPAIRS
        if EmeletSzam.get()     and isInt(EmeletSzam.get()):
            FLOORNUMBER     =   int(EmeletSzam.get())
            FLOORHEIGHT     =   SIZE[1] / FLOORNUMBER
        if LiftSzam.get()       and isInt(LiftSzam.get()):
            ELEVATORNUMBER  =   int(LiftSzam.get())
        if UtasSzam.get()       and isInt(UtasSzam.get()):
            PASSENGERNUMBER =   int(UtasSzam.get())
        if RandomSeed.get()     and isInt(RandomSeed.get()):
            SEED            =   int(RandomSeed.get())
            random.seed(SEED)
        if Idokoz.get()         and isInt(Idokoz.get()):
            TIMEINTERVALL   =   int(Idokoz.get())
            for i in range(PASSENGERNUMBER):
                spawnSecond = random.randint(1, TIMEINTERVALL)
                if spawnSecond in TIMEPASSENGERPAIRS:
                    TIMEPASSENGERPAIRS[spawnSecond] = TIMEPASSENGERPAIRS[spawnSecond] + 1
                    PASSENGERPAIRS[spawnSecond]     = PASSENGERPAIRS[spawnSecond] + 1
                else:
                    TIMEPASSENGERPAIRS[spawnSecond] = 1
                    PASSENGERPAIRS[spawnSecond]             = 1
        if AlapUtasSzam.get()   and isInt(AlapUtasSzam.get()):
            BASEPASSENGERS  = int(AlapUtasSzam.get())
        ALGORITHM       =   int(choicesValue.get())
        root.destroy()
        SCREEN          = pygame.display.set_mode(SIZE)
    root = tk.Tk()
    root.title('Data input')
    tk.Label(root, text = "Floor number:").grid(            row = 0, sticky = tk.W)
    tk.Label(root, text = "Elevator number:").grid(         row = 1, sticky = tk.W)
    tk.Label(root, text = "Passenger number:").grid(        row = 2, sticky = tk.W)
    tk.Label(root, text = "Time intervall:").grid(          row = 3, sticky = tk.W)
    tk.Label(root, text = "Base passenger number:").grid(   row = 4, sticky = tk.W)
    tk.Label(root, text = "Random seed:").grid(             row = 5, sticky = tk.W)
    EmeletSzam  = tk.Entry(root)
    LiftSzam    = tk.Entry(root)
    UtasSzam    = tk.Entry(root)
    Idokoz      = tk.Entry(root)
    AlapUtasSzam= tk.Entry(root)
    RandomSeed  = tk.Entry(root)
    EmeletSzam.grid(    row = 0, column = 1)
    LiftSzam.grid(      row = 1, column = 1)
    UtasSzam.grid(      row = 2, column = 1)
    Idokoz.grid(        row = 3, column = 1)
    AlapUtasSzam.grid(  row = 4, column = 1)
    RandomSeed.grid(    row = 5, column = 1)
    choicesValue = tk.IntVar()
    choices = [
        ("Algorithm 1 - Nearest Car"),
        ("Algorithm 2 - Sector"),
        ("Algorithm 3 - Up and Down"),
        ("Manual"),
    ]
    tk.Label(root, 
            text    =   "Select an algorithm: ",
            justify =   tk.LEFT,
            padx    =   20).grid(row = 6, sticky = tk.W)
    for val, choicess in enumerate(choices):
        tk.Radiobutton(root, 
                    text        =   choicess,
                    padx        =   20,
                    variable    =   choicesValue,
                    value       =   val,
                    indicator = 0, 
                    background = "light blue").grid(row = 7 + val, sticky = tk.W)
    tk.Button(root,
            text    =   "Submit",
            command =   getInput).grid(row = 11, sticky = tk.W)
    root.mainloop()
