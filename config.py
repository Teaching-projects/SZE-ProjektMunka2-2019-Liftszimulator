import pygame
import random
import tkinter as tk

pygame.init()
pygame.display.set_caption('Elevator simulator')

SIZE            = [1600, 900]
FLOORNUMBER     = 5
ELEVATORNUMBER  = 2
PASSENGERNUMBER = 10
FPS             = 60
FLOORHEIGHT     = SIZE[1] / FLOORNUMBER
SEED            = random.randint(0, 2 ** 10)
ALGORITHM       = 3
CLOCK           = pygame.time.Clock()
SCREEN          = pygame.display.set_mode(SIZE)
SMALLFONT       = pygame.font.SysFont(None, 16)

BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)

def menu():
    def getInput():
        if EmeletSzam.get():
            FLOORNUMBER     =   int(EmeletSzam.get())
            FLOORHEIGHT     =   SIZE[1] / FLOORNUMBER
        if LiftSzam.get():
            ELEVATORNUMBER  =   int(LiftSzam.get())
        if UtasSzam.get():
            PASSENGERNUMBER =   int(UtasSzam.get())
        if RandomSeed.get():
            SEED            =   int(RandomSeed.get())
        if choicesValue.get():
            ALGORITHM       =   int(choicesValue.get())
        root.destroy()
    root = tk.Tk()
    tk.Label(root, text = "Emeletek szama:").grid(  row = 0, sticky = tk.W)
    tk.Label(root, text = "Liftek szama:").grid(    row = 1, sticky = tk.W)
    tk.Label(root, text = "Utasok szama:").grid(    row = 2, sticky = tk.W)
    tk.Label(root, text = "Random seed:").grid(     row = 3, sticky = tk.W)
    EmeletSzam  = tk.Entry(root)
    LiftSzam    = tk.Entry(root)
    UtasSzam    = tk.Entry(root)
    RandomSeed  = tk.Entry(root)
    EmeletSzam.grid(row = 0, column = 1)
    LiftSzam.grid(  row = 1, column = 1)
    UtasSzam.grid(  row = 2, column = 1)
    RandomSeed.grid(row = 3, column = 1)
    choicesValue = tk.IntVar(0)
    choices = [
        ("Algorithm 1 - Nearest Car"),
        ("Algorithm 2 - Sector"),
        ("Algorithm 3 - "),
        ("Manual"),
    ]
    tk.Label(root, 
            text    =   "Select an algorithm: ",
            justify =   tk.LEFT,
            padx    =   20).grid(row = 4, sticky = tk.W)
    for val, choices in enumerate(choices):
        tk.Radiobutton(root, 
                    text        =   choices,
                    padx        =   20,
                    variable    =   choicesValue,
                    value       =   val).grid(row = 5 + val, sticky = tk.W)
    tk.Button(root,
            text    =   "Submit",
            command =   getInput).grid(row = 10, sticky = tk.W)
    root.mainloop()
