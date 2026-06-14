from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import Player


class PlayerStore:
    def __init__(self, save_dir: Path) -> None:
        self.path = save_dir / "players.json"
        save_dir.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def _read_all(self) -> dict[str, dict]:
        return json.loads(self.path.read_text(encoding="utf-8-sig"))

    def load(self, name: str, password: str) -> tuple[Player | None, str | None]:
        players = self._read_all()
        if name not in players:
            player = Player(name=name, password=password)
            self.save(player)
            return player, "새로운 퇴마사가 요새의 문 앞에 섰습니다."

        payload = players[name]
        if payload.get("password") != password:
            return None, "암호가 맞지 않습니다."
        return Player(**payload), "다시 요새로 돌아왔습니다."

    def save(self, player: Player) -> None:
        players = self._read_all()
        players[player.name] = asdict(player)
        self.path.write_text(json.dumps(players, ensure_ascii=False, indent=2), encoding="utf-8")

