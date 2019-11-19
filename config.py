import pygame

pygame.init()
pygame.display.set_caption('Elevator simulator')

SIZE            = [1200, 600]
FLOORNUMBER     = 10
ELEVATORNUMBER  = 5
PASSENGERNUMBER = 20
FPS             = 60
FLOORHEIGHT     = SIZE[1] / FLOORNUMBER
CLOCK           = pygame.time.Clock()
SCREEN          = pygame.display.set_mode(SIZE)
SMALLFONT       = pygame.font.SysFont(None, 16)

BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)


