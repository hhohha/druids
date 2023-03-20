from druids.agentMoving import AgentMoving
from druids.board import Board
from druids.enums import AgentType, Square
from druids.game import Team


class AgentStrong(AgentMoving):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.agentType = AgentType.STRONG
        self.startingAP = 1
        self.bagSize = 4
        self.sight = 1
        self.upgradeType = Square.GLOVES

    def can_pick_upgrade(self, square: Square) -> bool:
        return square == Square.GLOVES and not self.upgraded

    def upgrade(self) -> None:
        self.upgraded = True
        self.bagSize *= 2

    #def get_action(self):
    #    return Action(ActionType.SKIP)
