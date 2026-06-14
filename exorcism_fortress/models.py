from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Item:
    id: str
    name: str
    description: str


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
    inventory: list[str] = field(default_factory=list)
