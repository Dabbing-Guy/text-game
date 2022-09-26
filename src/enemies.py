"""Logic and Functions for the Turn-Based Combat System."""

import random
import time
import curses
from typing import List, Tuple, Dict, Any, Union, Optional, Sequence, TypeVar
import game_class


class Combatant:

    def __init__(self, name: str, hp: int, atk: int, turns: int, lvl: int,
                 skills: List[str]):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.turns = turns
        self.lvl = lvl
        self.skills = skills

    @classmethod
    def from_lvl(cls, name: str, lvl: int, skills: List[str]):
        """Create a combatant with stats based on a level"""
        hp = lvl * 8
        atk = lvl * 2
        turns = lvl // 5 + 1
        return cls(name, hp, atk, turns, lvl, skills)

    def attack(self, target) -> str:
        """Attack a target"""
        damage = random.randint(self.atk // 2, self.atk)
        target.hp -= damage
        return f"{self.name} attacked {target.name} for `b{damage} `ndamage."

    def __str__(self):
        return f"{self.name} (Lvl {self.lvl})"


class Slime(Combatant):

    def __init__(self, lvl: int, num: int):
        super().__init__(f"Slime {num}", lvl * 5 + random.randint(1, 2) * lvl,
                         lvl + random.randint(1, 2) * lvl, lvl // 8 + 1, lvl,
                         [""])


class Player(Combatant):

    def __init__(self, lvl: int, skills: List[str]):
        super().__init__("you", lvl * 6 + 15, lvl * 3, lvl // 5 + 1, lvl,
                         skills)

    # Functions for skills
    def punch(self, target: Combatant):
        """Punch the target"""
        attack = self.atk + random.randint(0, 3)
        target.hp -= attack
        return f"You punched {target.name} for {attack} damage."

    def sword_strike(self, target: Combatant):
        """Attack the target with your sword"""
        attack = self.atk * 2 + random.randint(0, 3)
        target.hp -= attack
        return f"You attacked {target.name} with your sword for `b{attack} `ndamage."
