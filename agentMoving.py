import random
from abc import ABC, abstractmethod
from collections import deque
from typing import List, Deque
from druids.agent import Agent
from druids.board import Pos
from druids.enums import ActionType, Direction, Square
from druids.game import Action


class AgentMoving(Agent, ABC):
    def __init__(self, team, board, strategy):
        super().__init__(team, board, strategy)
        self.bagSize = 0
        self.bag: List[Square] = []
        self.upgraded = False
        self.destinationPriority: int = 0
        self.currentPath: Deque[Pos] = deque()

        self.actions.update({
            ActionType.GO: self.perform_action_go,
            ActionType.PICK: self.perform_action_pick,
            ActionType.DIG: self.perform_action_dig,
            ActionType.DROP: self.perform_action_drop,
        })

    def perform_action_go(self, direction: Direction):
        if direction not in Direction:
            raise ValueError(f'invalid direction: {direction}')

        newPos = self.pos.go(direction)
        if not self.board.is_accessible(newPos):
            raise ValueError(f'cannot go to direction: {direction}')

        self.pos = newPos
        self.currentAP -= 1

    @abstractmethod
    def can_pick_upgrade(self, square: Square) -> bool:
        pass

    @abstractmethod
    def upgrade(self) -> None:
        pass

    def is_bag_full(self) -> bool:
        return len(self.bag) >= self.bagSize

    def perform_action_pick(self) -> None:
        square = self.board.get_square(self.pos)

        if square in [Square.GOLD, Square.TREE, Square.SCROLL]:
            if self.is_bag_full():
                raise ValueError(f'cannot pick, bag is full')
            self.bag.append(square)
            self.board.set_square(self.pos, Square.EMPTY)
        elif square == Square.WATER:
            if self.bagSize > 0:
                raise ValueError(f'cannot pick water, bag is not empty')
            self.bag = [Square.WATER] * self.bagSize
        elif self.can_pick_upgrade(square):
            self.upgrade()
            self.board.set_square(self.pos, Square.EMPTY)
        else:
            raise ValueError(f'cannot pick {square}')

        self.currentAP = 0

    def perform_action_dig(self, direction: Direction) -> None:
        digPos: Pos = self.pos.go(direction)
        if not self.board.in_bounds(digPos):
            raise ValueError(f'cannot dig out of bounds: {digPos}')
        if self.board.get_square(digPos) != Square.STONE:
            raise ValueError(f'no stone to dig: {digPos}')
        if self.is_bag_full():
            raise ValueError(f'cannot dig, bag is full')

        self.bag.append(Square.STONE)
        self.board.set_square(digPos, Square.EMPTY)
        print(f'agent {self} digging at {digPos}')
        self.currentAP = 0

    def perform_action_drop(self) -> None:
        if self.pos != self.board.basePos:
            raise ValueError('cannot drop, not in base')

        if self.bag:
            if self.bag[0] == Square.WATER:
                self.team.water += 1
            else:
                for item in self.bag:
                    if item == Square.TREE:
                        self.team.wood += 1
                    elif item == Square.GOLD:
                        self.team.gold += 1
                    elif item == Square.STONE:
                        self.team.stone += 1
                    elif item == Square.SCROLL:
                        self.team.scrolls += 1
                    else:
                        raise ValueError(f'something unexpected in my bag: {item}')
            self.bag = []
        self.currentAP = 0

    def choose_random_direction(self) -> Direction:
        availableDirs: List[Direction] = []
        for direction in Direction:
            if self.board.is_accessible(self.pos.go(direction)):
                availableDirs.append(direction)

        return random.choice(availableDirs)

    def look_for_base(self):
        if self.pos.x > self.board.basePos.x and self.board.is_accessible(self.pos.go(Direction.LEFT)):
            return Direction.LEFT
        if self.pos.x < self.board.basePos.x and self.board.is_accessible(self.pos.go(Direction.RIGHT)):
            return Direction.RIGHT
        if self.pos.y < self.board.basePos.y and self.board.is_accessible(self.pos.go(Direction.DOWN)):
            return Direction.DOWN
        if self.pos.y > self.board.basePos.y and self.board.is_accessible(self.pos.go(Direction.UP)):
            return Direction.UP

        return self.choose_random_direction()


    def get_action_simple(self) -> Action:
        """
        Simplest reasonable strategy
         - if at the base and got something - drop it
         - if location of upgrade is known and I don't have it yet - got there and pick it
         - if bag is full - go to the base
         - find the closest resource and go pick it
         - find the closest unknown square and explore it
        """
        if len(self.bag) > 0 and self.pos == self.board.basePos:
            return Action(ActionType.DROP)

        # am i already pursuing an upgrade?
        if self.destinationPriority == 10 and self.currentPath:
            nextPos: Pos = self.currentPath.popleft()
            if self.board.is_accessible(nextPos):
                return Action(ActionType.GO)

        if not self.upgraded and self.team.knownResourcesCtg[self.upgradeType]:
            self.destinationPriority = 10
            self.destination = self.find_closest(self.upgradeType)

        if self.destination:
            return Action(ActionType.GO, self.destination.pop())

        # can drop stuff - drop
        # can pickup or dig stuff - do it
        # am full - head to the base
        #

    get_action = get_action_simple
