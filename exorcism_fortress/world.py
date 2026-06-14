from __future__ import annotations

import json
from pathlib import Path

from .models import Item, Room


class World:
    def __init__(self, rooms: dict[str, Room], items: dict[str, Item]) -> None:
        self.rooms = rooms
        self.items = items

    @classmethod
    def load(cls, data_dir: Path) -> "World":
        rooms_data = json.loads((data_dir / "rooms.json").read_text(encoding="utf-8-sig"))
        items_data = json.loads((data_dir / "items.json").read_text(encoding="utf-8-sig"))
        rooms = {room_id: Room(id=room_id, **payload) for room_id, payload in rooms_data.items()}
        items = {item_id: Item(id=item_id, **payload) for item_id, payload in items_data.items()}
        return cls(rooms=rooms, items=items)

    def describe_room(self, room_id: str) -> str:
        room = self.rooms[room_id]
        lines = [f"[{room.name}]", room.description, ""]

        if room.items:
            visible_items = ", ".join(self.items[item_id].name for item_id in room.items if item_id in self.items)
            if visible_items:
                lines.append(f"보이는 물건: {visible_items}")

        if room.npcs:
            lines.append(f"마주친 존재: {', '.join(room.npcs)}")

        exits = ", ".join(room.exits.keys()) if room.exits else "없음"
        lines.append(f"출구: {exits}")
        return "\r\n".join(lines)

