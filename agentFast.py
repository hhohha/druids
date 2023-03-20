from druids.agentMoving import AgentMoving
from druids.board import Board
from druids.enums import AgentType, Square
from druids.game import Team


class AgentFast(AgentMoving):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.agentType = AgentType.FAST
        self.startingAP = 3
        self.bagSize = 2
        self.sight = 1
        self.upgradeType = Square.BOOTS

    def can_pick_upgrade(self, square: Square) -> bool:
        return square == Square.BOOTS and not self.upgraded

    def upgrade(self) -> None:
        self.upgraded = True
        self.actionPoints *= 2

    #def get_action(self):
    #    return Action(ActionType.SKIP)