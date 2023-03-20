from typing import List

from druids.agent import Agent
from druids.board import Board
from druids.config import SPELL_PAYOFFS
from druids.enums import AgentType, ActionType
from druids.game import Team, Spell, Action


class AgentDruid(Agent):
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


    def get_action_simple(self) -> Action:
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

    # set the current strategy
    get_action = get_action_simple
