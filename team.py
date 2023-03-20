from typing import Set, Dict

from druids.agentDruid import AgentDruid
from druids.agentFast import AgentFast
from druids.agentSharp import AgentSharp
from druids.agentStrong import AgentStrong
from druids.board import Board, Pos
from druids.enums import Color, Square, AgentType
from druids.game import Game, Spell, Action


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
        self.knownResourcesCtg: Dict[Square, Set[Pos]] = {}
        self.knownResources: Dict[Pos, Square] = {}
        self.spells: Set[Spell] = set()
        self.characters = [                 # TODO - agent factory
            AgentDruid(self, self.board, None),
            AgentFast(self, self.board, None),
            AgentStrong(self, self.board, None),
            AgentSharp(self, self.board, None)
        ]

    def play(self):
        for character in self.characters:
            startingPos = character.pos
            character.start_round()
            while character.has_action_points():
                self.update_known_board(character)     # TODO - optimize this, do it only when (to the extend which is) necessary
                action: Action = character.get_action()
                character.perform_action(action)
            if character.agentType != AgentType.DRUID:
                self.board.editedSquares.add(startingPos)
                self.board.characterSquares[(self.color, character.agentType)] = character.pos   # TODO - make the class character key

    def update_known_board(self, character):
        for pos, square in self.board.get_vision(character.pos, character.sight):
            if square == Square.EMPTY and pos in self.knownResources:
                # we saw a resource previously, but now it is not there
                self.knownResourcesCtg[square].remove(pos)
                del self.knownResources[pos]
                # we see a new resource, add it to known resources
            if square != Square.EMPTY and pos not in self.knownResources:
                self.knownResources[pos] = square
                self.knownResourcesCtg[square].add(pos)

            self.knownBoard.set_square(pos, square)

    def can_create_spell(self, spell: Spell) -> bool:
        return self.wood <= spell.wood and self.stone <= spell.stone and self.gold <= spell.gold and self.water <= spell.water