from abc import ABC, abstractmethod
from typing import Set, Dict, Callable, List
from board import Board, Pos
from dataclasses import dataclass
from config import SPELL_PAYOFFS
from enums import ActionType, Direction, Square, Color, AgentType
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

    def reset(self):    # TODO - implement
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

class Team:
    def __init__(self, game: Game, board: Board, strategy, color: Color):  # TODO: add color
        self.wood = 0
        self.gold = 0
        self.water = 0
        self.stone = 0
        self.scrolls = 0
        self.strategy = strategy
        self.points = 0
        self.board = board
        self.game = game
        self.color: Color = color
        self.knownBoard = Board(self.board.size)
        self.spells: Set[Spell] = set()
        self.characters = [
            Druid(self, self.board, None),
            Fast(self, self.board, None),
            Strong(self, self.board, None),
            Sharp(self, self.board, None)
        ]

    def play(self):
        for character in self.characters:
            startingPos = character.pos
            character.start_round()
            while character.has_action_points():
                self.update_known_board(character)     # TODO - optimize this, do it only when (to the extend which is) necessary
                action: Action = character.get_action()
                #print(f'agent {character}: {action}')
                character.perform_action(action)
            if character.agentType != AgentType.DRUID:
                self.board.editedSquares.add(startingPos)
                self.board.characterSquares[(self.color, character.agentType)] = character.pos   # TODO - make the class character key

    def update_known_board(self, character):
        for pos, square in self.board.get_vision(character.pos, character.sight):
            self.knownBoard.set_square(pos, square)

    def can_create_spell(self, spell: Spell) -> bool:
        return self.wood <= spell.wood and self.stone <= spell.stone and self.gold <= spell.gold and self.water <= spell.water

class Figure(ABC):
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

class MovingFigure(Figure, ABC):
    def __init__(self, team, board, strategy):
        super().__init__(team, board, strategy)
        self.bagSize = 0
        self.bag = []
        self.upgraded = False
        self.actions.update ({
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

    def get_action(self) -> Action:
        if self.bag and self.pos == self.board.basePos:
            return Action(ActionType.DROP)

        if self.is_bag_full():
            return Action(ActionType.GO, self.look_for_base())

        square = self.board.get_square(self.pos)
        if square in [Square.WATER, Square.TREE, Square.SCROLL, Square.GOLD] or self.can_pick_upgrade(square):
            return Action(ActionType.PICK)

        for direction in Direction:
            digPos = self.pos.go(direction)
            if self.board.in_bounds(digPos) and self.board.get_square(digPos) == Square.STONE:
                return Action(ActionType.DIG, direction)

        return Action(ActionType.GO, self.choose_random_direction())

class Druid(Figure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.startingAP = 1
        self.sight = 0
        self.bagSize = 0
        self.agentType = AgentType.DRUID
        self.actions.update({
            ActionType.READ: self.perform_action_read,
            ActionType.CREATE: self.perform_action_create,
            ActionType.PROPOSE: self.perform_action_propose,
            ActionType.ACCEPT: self.perform_action_accept,
        })

    def perform_action_read(self, scrollCnt):
        if scrollCnt > self.team.scrolls:
            raise ValueError(f'not enough scrolls to read {scrollCnt}')
        if scrollCnt not in SPELL_PAYOFFS:
            raise ValueError(f'it is not possible to read {scrollCnt} scrolls')

        self.team.scrolls -= scrollCnt
        newSpell = self.team.game.generate_spell(scrollCnt)
        self.team.spells.add(newSpell)

        self.currentAP = 0

    def perform_action_create(self, spell: Spell):
        if self.team.gold < spell.gold:
            raise ValueError('not enough gold for this spell')
        if self.team.wood < spell.wood:
            raise ValueError('not enough gold for this spell')
        if self.team.water < spell.water:
            raise ValueError('not enough gold for this spell')
        if self.team.stone < spell.stone:
            raise ValueError('not enough gold for this spell')
        self.team.gold -= spell.gold
        self.team.wood -= spell.wood
        self.team.water -= spell.water
        self.team.stone-= spell.stone
        self.team.points += spell.payoff

        self.currentAP = 0

    def perform_action_propose(self):
        self.currentAP = 0

    def perform_action_accept(self):
        self.currentAP = 0

    def get_available_spells(self) -> List[Spell]:
        return list(filter(self.team.can_create_spell, self.team.spells))   # TODO - remove list

    def get_action(self) -> Action:
        if self.team.scrolls >= 3:
            return Action(ActionType.READ, 3)

        availableSpells = self.get_available_spells()
        if availableSpells:
            return Action(ActionType.CREATE, availableSpells[0])

        return Action(ActionType.SKIP)


class Sharp(MovingFigure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.agentType = AgentType.SHARP
        self.startingAP = 2
        self.bagSize = 1
        self.sight = 3

    def can_pick_upgrade(self, square: Square) -> bool:
        return square == Square.GLASSES and not self.upgraded

    def upgrade(self) -> None:
        self.upgraded = True
        self.sight *= 2

class Strong(MovingFigure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.agentType = AgentType.STRONG
        self.startingAP = 1
        self.bagSize = 4
        self.sight = 1

    def can_pick_upgrade(self, square: Square) -> bool:
        return square == Square.GLOVES and not self.upgraded

    def upgrade(self) -> None:
        self.upgraded = True
        self.bagSize *= 2

    #def get_action(self):
    #    return Action(ActionType.SKIP)

class Fast(MovingFigure):
    def __init__(self, team: Team, board: Board, strategy):
        super().__init__(team, board, strategy)
        self.agentType = AgentType.FAST
        self.startingAP = 3
        self.bagSize = 2
        self.sight = 1

    def can_pick_upgrade(self, square: Square) -> bool:
        return square == Square.BOOTS and not self.upgraded

    def upgrade(self) -> None:
        self.upgraded = True
        self.actionPoints *= 2

    #def get_action(self):
    #    return Action(ActionType.SKIP)

