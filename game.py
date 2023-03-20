from typing import Set, Dict, Callable, List
from board import Board, Pos
from enums import ActionType, Direction, Square, Color, AgentType

from typing import List
from dataclasses import dataclass
from config import SPELL_PAYOFFS
from druids.team import Team
from enums import ActionType, Color
import random


@dataclass(frozen=True)
class Spell:
    gold: int
    stone: int
    water: int
    wood: int
    payoff: int


class Action:
    def __init__(self, actionType: ActionType, param=None):
        self.actionType = actionType
        self.param = param


class Game:
    def __init__(self, board, teamCnt: int):
        self.running = False
        self.board = board
        self.teams = [Team(self, self.board, None, Color.BLACK)] * teamCnt
        self.steps = 0
        self.generate_starting_spells()

    def reset(self):  # TODO - implement
        pass

    def run(self):
        self.running = True

    def pause(self):
        self.running = False

    def step(self):
        for team in self.teams:
            team.play()

    def generate_starting_spells(self):
        for _ in range(random.randint(1, 6)):
            spell = self.generate_spell(0)
            for team in self.teams:
                team.spells.add(spell)

    @staticmethod
    def generate_spell(scrolls: int) -> Spell:
        if scrolls not in SPELL_PAYOFFS:
            raise ValueError(f'cannot generate spell from {scrolls} scrolls')

        resources: List[int] = [0, 0, 0, 0]
        for _ in range(scrolls):
            resources[random.randint(0, 3)] += 1
        #return Spell(*resources, SPELL_PAYOFFS[scrolls])
        return Spell(resources[0], resources[1], resources[2], resources[3], SPELL_PAYOFFS[scrolls])
