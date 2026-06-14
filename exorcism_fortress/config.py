from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 6666
    encoding: str = "utf-8"
    command_cooldown_seconds: float = 1.0
    data_dir: Path = Path("data")
    save_dir: Path = Path("saves")
    log_dir: Path = Path("logs")


SUPPORTED_ENCODINGS = ("utf-8", "cp949", "euc-kr")
