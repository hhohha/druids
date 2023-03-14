from abc import ABC, abstractmethod

class cTeam:
    def __init__(self, teamStrategy):
        self.wood = 0
        self.gold = 0
        self.water = 0
        self.stone = 0
        self.strategy = teamStrategy

        self.characters = [cDruid(), cFast(), cStrong(), cSharp()]

    def play(self):
        for character in self.characters:
            character.play()

class cFigure(ABC):
    def __init__(self):
        coorx = None
        coory = None
        bag = []

    @abstractmethod
    def play(self):
        pass

class cDruid(cFigure):
    def play(self):
        pass

class cSharp(cFigure):
    def play(self):
        pass

class cStrong(cFigure):
    def play(self):
        pass

class cFast(cFigure):
    def play(self):
        pass
