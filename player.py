"""Defines a player. This will eventually hold all the creation factories for
the various classes."""
import logging
from jfighter import Fighter, Skill
from monster import Monster
from items import weapon

log = logging.getLogger(__name__)

class Player(Monster):
    """Players are controllable monsters. In theory, we could find a way to let
    multiple players exist in the game and take action in turn?"""
    def __init__(self, x, y, level,game):
        Monster.__init__(self, x=x, y=y, game=game, name="player", disp="@",
                         color="Player",
                         description="A hero of might and courage.",
                         blocks=True,
                         fighter_comp=Fighter(st=14,dx=12,iq=14,ht=14))
        self.fighter_comp.equipped['right hand'] = weapon.Weapon('Longsword',
                                                                 ')', 'player',
                                                                 game, None, 5,
                                                                 'slashing', self,
                                                                 'Longswords')
        self.fighter_comp.add_skill("Longswords", 'ST', 10, 0, 'attack')
        self.fighter_comp.add_skill("Defense", 'DX', 0, 0, 'defense')

    def died(self):
        self.game_instance.save_game(None)

    def rest(self):
        self.fighter_comp.heal(1)
