from abc import ABC, abstractmethod
from typing import Dict, Callable
from druids.board import Board, Pos
from druids.enums import ActionType
from druids.game import Team, Action


class Agent(ABC):
    def __init__(self, team: Team, board: Board, strategy):
        self.pos: Pos = board.basePos
        self.currentAP: int = 0
        self.startingAP: int = 0
        self.team = team
        self.board: Board = board
        self.strategy = strategy
        self.actions: Dict[ActionType, Callable] = {
            ActionType.SKIP: self.perform_action_skip
        }

    def perform_action(self, action: Action) -> None:
        if action.actionType not in self.actions:
            raise ValueError('bad action')
        if action.param is None:
            self.actions[action.actionType]()
        else:
            self.actions[action.actionType](action.param)

    def has_action_points(self) -> bool:
        return self.currentAP > 0

    def start_round(self):
        self.currentAP = self.startingAP

    def perform_action_skip(self):
        self.currentAP = 0

    @abstractmethod
    def get_action(self) -> Action:
        pass
