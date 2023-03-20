import random
from typing import Dict, Tuple, Set

from config import *
from math import sqrt
from dataclasses import dataclass
from enums import Square, Direction, Color, AgentType


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def go(self, direction: Direction) -> 'Pos':
        if direction == Direction.UP:
            return Pos(self.x, self.y-1)
        if direction == Direction.DOWN:
            return Pos(self.x, self.y+1)
        if direction == Direction.LEFT:
            return Pos(self.x-1, self.y)
        if direction == Direction.RIGHT:
            return Pos(self.x+1, self.y)
        raise ValueError(f'invalid direction: {direction}')

def distance(p1: Pos, p2: Pos) -> float:
    return sqrt(abs(p1.x - p2.x)**2 + abs(p1.y - p2.y)**2)

class Board:
    def __init__(self, size: Pos):
        self.size: Pos = size
        self.squares = [Square.EMPTY] * size.x * size.y
        self.editedSquares: Set[Pos] = set()
        self.basePos: Pos = Pos(0, 0)
        self.characterSquares: Dict[Tuple[Color, AgentType], Pos] = {}

    def clear(self):
        self.squares = [Square.EMPTY] * self.size.x * self.size.y
        self.editedSquares = set()

    def edited_squares(self):
        while self.editedSquares:
            yield self.editedSquares.pop()

    def get_square(self, p: Pos):
        return self.squares[p.x + self.size.x*p.y]

    def in_bounds(self, p: Pos):
        return 0 <= p.x < self.size.x and 0 <= p.y < self.size.y

    def is_accessible(self, pos: Pos) -> bool:
        return self.in_bounds(pos) and self.get_square(pos) not in [Square.STONE]

    def move_square(self, pFrom: Pos, pTo: Pos):
        self.set_square(pTo, self.get_square(pFrom))
        self.set_square(pFrom, Square.EMPTY)

    def set_square(self, p: Pos, value):
        self.squares[p.x + self.size.x*p.y] = value
        self.editedSquares.add(p)

    def get_vision(self, pos: Pos, sight: int):
        startX = max(pos.x - sight, 0)
        startY = max(pos.y - sight, 0)
        endX = min(pos.x + sight + 1, self.size.x)
        endY = min(pos.y + sight + 1, self.size.y)

        for x, y in zip(range(startX, endX), range(startY, endY)):
            yield Pos(x, y), self.get_square(Pos(x, y))

    def place_stone(self, p: Pos, size: int):
        if not self.in_bounds(p):
            return
        self.set_square(p, Square.STONE)

        if size > 1:
            self.place_stone(Pos(p.x+1, p.y), size-1)
            self.place_stone(Pos(p.x-1, p.y), size-1)
            self.place_stone(Pos(p.x, p.y+1), size-1)
            self.place_stone(Pos(p.x, p.y-1), size-1)

    def place_water_ellipse(self, centre1: Pos, centre2: Pos, p: Pos, radius):
        if not self.in_bounds(p) or self.get_square(p) == Square.WATER:
            return

        if distance(p, centre1) + distance(p, centre2) > radius:
            return

        self.set_square(p, Square.WATER)

        self.place_water_ellipse(centre1, centre2, Pos(p.x+1, p.y), radius)
        self.place_water_ellipse(centre1, centre2, Pos(p.x-1, p.y), radius)
        self.place_water_ellipse(centre1, centre2, Pos(p.x, p.y+1), radius)
        self.place_water_ellipse(centre1, centre2, Pos(p.x, p.y-1), radius)

    def find_empty_square(self) -> Pos:
        i = 0

        while True:
            p = Pos(random.randrange(0, self.size.x), random.randrange(0, self.size.y))
            if self.get_square(p) == Square.EMPTY:
                return p

            if i == 100:
                raise RuntimeError("Cannot find an empty square")
            i += 1

    def generate_map(self, seed):
        self.clear()
        random.seed(seed)

        for centresDistance, radius in LAKES:
            p1 = self.find_empty_square()
            p2 = Pos(p1.x + random.randrange(0, centresDistance), p1.y + random.randrange(0, centresDistance))
            self.place_water_ellipse(p1, p2, p1, distance(p1, p2) + radius)


        for forestSize, density in FORESTS:
            # forest centre
            p1 = self.find_empty_square()

            for maxOffset in range(2, forestSize):
                for i in range(density):
                    offset = Pos(random.randrange(-maxOffset, maxOffset+1), random.randrange(-maxOffset, maxOffset+1))
                    p2 = Pos(p1.x + offset.x, p1.y + offset.y)
                    if self.in_bounds(p2) and self.get_square(p2) == Square.EMPTY:
                        self.set_square(p2, Square.TREE)

        for i in range(GOLDS):
            self.set_square(self.find_empty_square(), Square.GOLD)

        for i in range(LONELY_TREES):
            self.set_square(self.find_empty_square(), Square.TREE)

        for stoneSize in STONES:
            self.place_stone(self.find_empty_square(), stoneSize)

        self.basePos = self.find_empty_square()
        self.set_square(self.basePos, Square.BASE)

        for _ in range(BOOTS_CNT):
            self.set_square(self.find_empty_square(), Square.BOOTS)
        for _ in range(GLOVES_CNT):
            self.set_square(self.find_empty_square(), Square.GLOVES)
        for _ in range(GLASSES_CNT):
            self.set_square(self.find_empty_square(), Square.GLASSES)

        for _ in range(SCROLL_CNT):
            self.set_square(self.find_empty_square(), Square.SCROLL)