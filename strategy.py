from dataclasses import dataclass
from typing import Callable, List, Optional, Set
from sortedcollections import SortedSet

from board import Pos, Board
from enums import ActionType, Direction, Square
from game import Druid, Action, MovingFigure


@dataclass
class Strategy:
        druid: Callable
        sharp: Callable
        fast: Callable
        strong: Callable

def druid_get_action_simple(self: Druid) -> Action:
    """
    Simplest reasonable strategy
     - read scrolls immediately when possible
     - create spells immediately when possible
     - propose no coalitions
     - accept no coalition
     - define no priorities for others
    """
    if self.team.scrolls >= 3:
        return Action(ActionType.READ, 3)

    availableSpells = self.get_available_spells()
    if availableSpells:
        return Action(ActionType.CREATE, availableSpells[0])

    return Action(ActionType.SKIP)

class Node:
    def __init__(self, parent: Optional['Node'], pos: Pos, dest: Pos):
        self.parent = parent
        self.pos = pos
        self.cost = 0 if parent is None else parent.cost + 1
        self.dest = dest
        self.estimate = self.countEstimate()

    def countEstimate(self) -> int:
        return -(self.cost + abs(self.pos.x - self.dest.x) + abs(self.pos.y - self.dest.y))

    def updateCost(self, cost):
        self.cost = cost
        self.estimate = self.countEstimate()

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.estimate < other.estimate

    def __hash__(self) -> int:
        return hash(self.pos)

    def __str__(self):
        return f'Node({self.pos.x}, {self.pos.y})'

    __repr__ = __str__

def find_path_a_star(board: Board, posFrom: Pos, posTo: Pos) -> List[Pos]:
    nodes: SortedSet[Node] = SortedSet()
    nodes.add(Node(None, posFrom, posTo))
    closedPos: Set[Pos] = set()

    while nodes:
        curNode = nodes.pop()
        for direction in Direction:
            newPos = curNode.pos.go(direction)
            if newPos in closedPos:
                continue
            else:
                closedPos.add(newPos)
            if not board.in_bounds(newPos) or not board.is_accessible(newPos):
                continue

            newNode = Node(curNode, newPos, posTo)
            if newNode.pos == posTo:
                backTrackNode = newNode
                result: List[Pos] = []
                while backTrackNode.parent is not None:
                    result.append(backTrackNode.pos)
                    backTrackNode = backTrackNode.parent
                    board.set_square(backTrackNode.pos, Square.WATER)
                return result

            if newNode not in nodes:
                nodes.add(newNode)
                board.set_square(newNode.pos, Square.GOLD)
    return []


def moving_get_action_simple(self: MovingFigure) -> Action:
    pass