from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Item:
    id: str
    name: str
    description: str


@dataclass
class Npc:
    id: str
    name: str
    description: str
    hp: int
    max_hp: int
    attack: int
    exp_reward: int = 0
    hostile: bool = False
    dialogue: list[str] = field(default_factory=list)


@dataclass
class Room:
    id: str
    name: str
    description: str
    exits: dict[str, str]
    items: list[str] = field(default_factory=list)
    npcs: list[str] = field(default_factory=list)


@dataclass
class Player:
    name: str
    password: str
    room_id: str = "gate"
    hp: int = 30
    max_hp: int = 30
    attack: int = 6
    exp: int = 0
    inventory: list[str] = field(default_factory=list)
    equipment: list[str] = field(default_factory=list)
