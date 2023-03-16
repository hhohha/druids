from abc import ABC, abstractmethod
from board import Pos

class Game:
    def __init__(self, board, teamCnt: int):
        self.running = False
        self.board = board
        self.teams = [Team] * teamCnt
        self.steps = 0

    def run(self):
        self.running = True

    def pause(self):
        self.running = False

    def step(self):
        for team in self.teams:
            team.play()

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
            character.start_round()
            while character.has_action_points():
                character.play()

class Figure(ABC):
    def __init__(self):
        self.pos: Pos
        self.bag = []
        self.currentAP: int = 0
        self.startingAP: int = 0

    def has_action_points(self) -> bool:
        return self.currentAP > 0

    def start_round(self):
        self.currentAP = self.startingAP

    @abstractmethod
    def play(self):
        pass


class MovingFigure(Figure, ABC):
    def __init__(self):
        super().__init__()
        self.bagSize = 0

    def has_space(self):
        return len(self.bag) < self.bagSize

class Druid(Figure):
    def __init__(self):
        super().__init__()
        self.startingAP = 1

    def play(self):
        pass

class Sharp(Figure):
    def __init__(self):
        super().__init__()
        self.startingAP = 2
        self.bagSize = 1
        self.sight = 3

    def play(self):
        pass

class Strong(Figure):
    def __init__(self):
        super().__init__()
        self.startingAP = 1
        self.bagSize = 4
        self.sight = 1

    def play(self):
        pass

class Fast(Figure):
    def __init__(self):
        super().__init__()
        self.actionPoints = 3
        self.bagSize = 2
        self.sight = 1

    def play(self):
        pass
