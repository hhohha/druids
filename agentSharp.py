from druids.agentMoving import AgentMoving
from druids.board import Board
from druids.enums import AgentType, Square
from druids.game import Team


class AgentSharp(AgentMoving):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.agentType = AgentType.SHARP
        self.startingAP = 2
        self.bagSize = 1
        self.sight = 3
        self.upgradeType = Square.GLASSES

    def can_pick_upgrade(self, square: Square) -> bool:
        return square == Square.GLASSES and not self.upgraded

    def upgrade(self) -> None:
        self.upgraded = True
        self.sight *= 2