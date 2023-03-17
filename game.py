from abc import ABC, abstractmethod
from board import Pos, Board, Square
from enum import Enum
from dataclasses import dataclass
import random

SPELL_MAKER = {
    3: 4,
    4: 6,
    5: 9
}

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class ActionType(Enum):
    GO = 0
    PICK = 1
    DIG = 2
    DROP = 3
    SKIP = 4
    READ = 5
    CREATE = 6
    PROPOSE = 7
    ACCEPT = 8

@dataclass
class Spell:
    gold: int
    stone: int
    water: int
    wood: int
    payoff: int

class Action:
    def __init__(self, actionType: ActionType, param=None):
        pass

class Game:
    def __init__(self, board, teamCnt: int):
        self.running = False
        self.board = board
        self.teams = [Team(self, self.board, None)] * teamCnt
        self.steps = 0

    def run(self):
        self.running = True

    def pause(self):
        self.running = False

    def step(self):
        for team in self.teams:
            team.play()

    def generate_spell(self, scrolls: int) -> Spell:
        if scrolls not in SPELL_MAKER:
            raise ValueError(f'cannot generate spell from {scrolls} scrolls')

        resources = [0, 0, 0, 0]
        for _ in range(scrolls):
            resources[random.randint(0, 3)] += 1
        return Spell(*resources, SPELL_MAKER[scrolls])

class Team:
    def __init__(self, game, board, strategy):  # TODO: add color
        self.wood = 0
        self.gold = 0
        self.water = 0
        self.stone = 0
        self.scrolls = 0
        self.strategy = strategy
        self.board = board
        self.knownBoard = Board(self.board.size)
        self.spells = []
        self.characters = [
            Druid(self, self.board, strategy.druid),
            Fast(self, self.board, strategy.fast),
            Strong(self, self.board, strategy.strong),
            Sharp(self, self.board, strategy.sharp)
        ]

    def play(self):
        for character in self.characters:
            character.start_round()
            while character.has_action_points():
                self.update_known_board(character)     # TODO - optimize this, do it only when (to the extend which is) necessary
                action = character.get_action()
                self.board.make_action(action)

    def update_known_board(self, character):
        for pos, square in self.board.get_vision(character.pos, character.sight):
            self.knownBoard.set_square(pos, square)

class Figure(ABC):
    def __init__(self, team: Team, board: Board, strategy):
        self.pos = board.basePos
        self.currentAP: int = 0
        self.startingAP: int = 0
        self.team = team
        self.board = board
        self.strategy = strategy

    def perform_action(self, action: Action) -> None:
        if action.actionType not in self.actions:
            raise ValueError('bad action')

        self.actions[ActionType](action.param)

    def has_action_points(self) -> bool:
        return self.currentAP > 0

    def start_round(self):
        self.currentAP = self.startingAP

    def perform_action_skip(self):
        pass

    @abstractmethod
    def get_action(self) -> Action:
        pass

class MovingFigure(Figure, ABC):
    def __init__(self):
        super().__init__()
        self.bagSize = 0
        self.bag = []
        self.actions = {
            ActionType.GO: self.perform_action_go,
            ActionType.PICK: self.perform_action_pick,
            ActionType.PICK: self.perform_action_pick,
            ActionType.DIG: self.perform_action_dig,
            ActionType.DROP: self.perform_action_drop,
            ActionType.SKIP: self.perform_action_skip,
        }

    def perform_action_go(self):
        pass

    def perform_action_pick(self):
        pass

    def perform_action_dig(self):
        pass

    def perform_action_drop(self):
        pass

class Druid(Figure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.startingAP = 1
        self.sight = 0
        self.bagSize = 0
        self.actions = {
            ActionType.READ: self.perform_action_read,
            ActionType.CREATE: self.perform_action_create,
            ActionType.PROPOSE: self.perform_action_propose,
            ActionType.ACCEPT: self.perform_action_accept,
            ActionType.SKIP: self.perform_action_skip,
        }

    def perform_action_read(self, scrollCnt):
        if scrollCnt > self.team.scrolls:
            raise ValueError('not enough scrolls')
        if scrollCnt not in SPELL_MAKER:
            raise ValueError(f'cannot read {scrollCnt} scrolls')

        self.team.scrolls -= scrollCnt
        newSpell = self.team.game.generate_spell(scrollCnt)
        self.team.addSpell(newSpell)

    def perform_action_create(self):
        pass

    def perform_action_propose(self):
        pass

    def perform_action_accept(self):
        pass


    def play(self):
        action = self.get_action()
        self.perform_action()

    def get_action(self):
        pass



class Sharp(Figure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy))
        self.startingAP = 2
        self.bagSize = 1
        self.sight = 3

    def get_action(self):
        pass

class Strong(Figure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.startingAP = 1
        self.bagSize = 4
        self.sight = 1

    def get_action(self):
        pass

class Fast(Figure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.actionPoints = 3
        self.bagSize = 2
        self.sight = 1

    def get_action(self):
        pass
