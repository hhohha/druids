import random
from config import *
from math import sqrt

SQR_EMPTY = 'empty'
SQR_WOOD = 'tree'
SQR_GOLD = 'gold'
SQR_STONE = 'stone'
SQR_WATER = 'water'
SQR_BASE = 'base'
SQR_BOOTS = 'boots'
SQR_GLASSES = 'glasses'
SQR_GLOVES = 'gloves'

def distance(x1, y1, x2, y2):
    return sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)

class cSquare:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class cBoard:
    def __init__(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.squares = [SQR_EMPTY] * sizex * sizey
        self.editedSquares = set()

    def clear(self):
        self.squares = [SQR_EMPTY] * self.sizex * self.sizey
        self.editedSquares = set()

    def edited_squares(self):
        while self.editedSquares:
            yield self.editedSquares.pop()

    def get_square(self, x, y):
        return self.squares[x + self.sizex*y]

    def in_bounds(self, x, y):
        return 0 <= x < self.sizex and 0 <= y < self.sizey

    def move_square(self, fromX, fromY, toX, toY):
        self.set_square(toX, toY, self.get_square(fromX, fromY))
        self.set_square(fromX, fromY, SQR_EMPTY)

    def set_square(self, x, y, value):
        self.squares[x + self.sizex*y] = value
        self.editedSquares.add(cSquare(x, y))

    def place_stone(self, x, y, size):
        if not self.in_bounds(x, y):
            return
        self.set_square(x, y, SQR_STONE)

        if size > 1:
            self.place_stone(x+1, y, size-1)
            self.place_stone(x-1, y, size-1)
            self.place_stone(x, y+1, size-1)
            self.place_stone(x, y-1, size-1)

    def place_water_ellipse(self, centre1X, centre1Y, centre2X, centre2Y, x, y, radius):
        if not self.in_bounds(x, y):
            return

        if self.get_square(x, y) == SQR_WATER:
            return

        if distance(x, y, centre1X, centre1Y) + distance(x, y, centre2X, centre2Y) > radius:
            return

        self.set_square(x, y, SQR_WATER)

        self.place_water_ellipse(centre1X, centre1Y, centre2X, centre2Y, x+1, y, radius)
        self.place_water_ellipse(centre1X, centre1Y, centre2X, centre2Y, x-1, y, radius)
        self.place_water_ellipse(centre1X, centre1Y, centre2X, centre2Y, x, y+1, radius)
        self.place_water_ellipse(centre1X, centre1Y, centre2X, centre2Y, x, y-1, radius)

    def find_empty_square(self):
        i = 0

        while True:
            x, y = random.randrange(0, self.sizex), random.randrange(0, self.sizey)
            if self.get_square(x, y) == SQR_EMPTY:
                return x, y

            if i == 100:
                raise RuntimeError("Cannot find an empty square")
            i += 1


    def generate_map(self, seed):
        self.clear()
        random.seed(seed)

        for centresDistance, radius in LAKES:
            x1, y1 = self.find_empty_square()
            x2, y2 = x1 + random.randrange(0, centresDistance), y1 + random.randrange(0, centresDistance)
            self.place_water_ellipse(x1, y1, x2, y2, x1, y1, distance(x1, y1, x2, y2) + radius)


        for forestSize, density in FORESTS:
            # forest centre
            x, y = self.find_empty_square()

            for maxOffset in range(2, forestSize):
                for i in range(density):
                    xoffset = random.randrange(-maxOffset, maxOffset+1)
                    yoffset = random.randrange(-maxOffset, maxOffset+1)
                    if self.in_bounds(x + xoffset, y + yoffset) and self.get_square(x + xoffset, y + yoffset) == SQR_EMPTY:
                        self.set_square(x + xoffset, y + yoffset, SQR_WOOD)

        for i in range(GOLDS):
            self.set_square(*self.find_empty_square(), SQR_GOLD)

        for i in range(LONELY_TREES):
            self.set_square(*self.find_empty_square(), SQR_WOOD)

        for stoneSize in STONES:
            self.place_stone(*self.find_empty_square(), stoneSize)

        self.set_square(*self.find_empty_square(), SQR_BASE)

        for _ in range(BOOTS_CNT):
            self.set_square(*self.find_empty_square(), SQR_BOOTS)
        for _ in range(GLOVES_CNT):
            self.set_square(*self.find_empty_square(), SQR_GLOVES)
        for _ in range(GLASSES_CNT):
            self.set_square(*self.find_empty_square(), SQR_GLASSES)
