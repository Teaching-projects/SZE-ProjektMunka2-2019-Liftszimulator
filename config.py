import pygame
import tkinter as tk

pygame.init()
pygame.display.set_caption('Elevator simulator')




SIZE            = [1200, 600]
FLOORNUMBER     = None
ELEVATORNUMBER  = None
PASSENGERNUMBER = None
FPS             = 60
FLOORHEIGHT     = None
SEED            = None
CLOCK           = pygame.time.Clock()
SCREEN          = pygame.display.set_mode(SIZE)
SMALLFONT       = pygame.font.SysFont(None, 16)

BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)


def menu():
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
    UtasSzam.grid(row = 2, column = 1)
    RandomSeed.grid(row = 3, column = 1)

    def getInput():

        a = EmeletSzam.get()
        b = LiftSzam.get()
        c = UtasSzam.get()
        d = RandomSeed.get()
        e = v.get()
        root.destroy()

        
        global FLOORNUMBER
        FLOORNUMBER=int(a)
        global ELEVATORNUMBER
        ELEVATORNUMBER=int(b)
        global PASSENGERNUMBER
        PASSENGERNUMBER=int(c)
        global FLOORHEIGHT
        FLOORHEIGHT=SIZE[1] / FLOORNUMBER
        global SEED
        SEED=int(d)

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
            justify = tk.LEFT,
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
