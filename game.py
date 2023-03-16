from abc import ABC, abstractmethod
from board import Pos

class Game:
    def __init__(self, teamCnt: int):
        self.running = False
        self.board = None
        self.teams = [Team] * teamCnt

    def start(self):
        self.running = True

class Team:
    def __init__(self, teamStrategy):
        self.wood = 0
        self.gold = 0
        self.water = 0
        self.stone = 0
        self.strategy = teamStrategy

        self.characters = [Druid(), Fast(), Strong(), Sharp()]

    def play(self):
        for character in self.characters:
            character.play()

class Figure(ABC):
    def __init__(self):
        self.pos: Pos
        self.bag = []

    @abstractmethod
    def play(self):
        pass

class Druid(Figure):
    def play(self):
        pass

class Sharp(Figure):
    def play(self):
        pass

class Strong(Figure):
    def play(self):
        pass

class Fast(Figure):
    def play(self):
        pass
