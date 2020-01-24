import pygame

pygame.init()
pygame.display.set_caption('Elevator simulator')

SIZE            = [1600, 900]
FLOORNUMBER     = 20
ELEVATORNUMBER  = 6
PASSENGERNUMBER = 200
FPS             = 120
FLOORHEIGHT     = SIZE[1] / FLOORNUMBER
FLOORWIDTH      = 90
FLOORDISTANCE   = 100
CLOCK           = pygame.time.Clock()
SCREEN          = pygame.display.set_mode(SIZE)
SMALLFONT       = pygame.font.SysFont(None, 16)

BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)


