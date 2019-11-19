from pygame import Rect

class Rectangle:
    def __init__(self, x, y, width, height, master = False):
        self.X      = x
        self.Y      = y
        self.Width  = width
        self.Height = height
        self.Master = master
        if self.Master:
            self.Upper = Rectangle(x, y+1, width, height / 8)
            self.Lower = Rectangle(x, y+(7 * height / 8), width, height / 8)
        else:         
            self.Upper = 0
            self.Lower = 0
    def getRectangle(self): return Rect(self.X, self.Y, self.Width, self.Height)
    def move(self, y):      self.Y += y
    def getUpper(self):     return self.Upper
    def getLower(self):     return self.Lower
    def getX(self):         return self.X
    def getY(self):         return self.Y
    def getWidth(self):     return self.Width
    def getHeight(self):    return self.Height