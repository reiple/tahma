from __future__ import annotations

import argparse
import socket
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SUPPORTED_ENCODINGS = ("utf-8", "cp949", "euc-kr")
DEFAULT_HOST = "xmud.ddnsfree.com"
DEFAULT_PORT = 6666
MIN_COMMAND_INTERVAL_SECONDS = 1.5
MAX_COMMANDS_PER_SESSION = 8
MAX_SESSION_SECONDS = 60.0
READ_TIMEOUT_SECONDS = 3.0


@dataclass(frozen=True)
class ObservationConfig:
    host: str
    port: int
    name: str
    password: str
    commands: list[str]
    preferred_encoding: str
    output_dir: Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safely observe a Korean text MUD server with strict rate limits."
    )
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--name", default="심리학과")
    parser.add_argument("--password", default="심리학과")
    parser.add_argument("--commands-file", type=Path, required=True)
    parser.add_argument("--encoding", choices=SUPPORTED_ENCODINGS, default="cp949")
    parser.add_argument("--output-dir", type=Path, default=Path("logs") / "observations")
    return parser


def load_commands(path: Path) -> list[str]:
    commands = [
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if len(commands) > MAX_COMMANDS_PER_SESSION:
        raise SystemExit(
            f"Too many commands: {len(commands)}. "
            f"Limit each observation session to {MAX_COMMANDS_PER_SESSION} commands."
        )
    return commands


def read_available(sock: socket.socket, deadline: float) -> bytes:
    chunks: list[bytes] = []
    while time.monotonic() < deadline:
        try:
            chunk = sock.recv(8192)
        except TimeoutError:
            break
        if not chunk:
            break
        chunks.append(chunk)
        if len(chunk) < 8192:
            time.sleep(0.2)
    return b"".join(chunks)


def decode_all(raw: bytes, preferred_encoding: str) -> dict[str, str]:
    order = [preferred_encoding, *[enc for enc in SUPPORTED_ENCODINGS if enc != preferred_encoding]]
    decoded: dict[str, str] = {}
    for encoding in order:
        decoded[encoding] = raw.decode(encoding, errors="replace")
    return decoded


def write_logs(config: ObservationConfig, raw: bytes, sent_commands: list[str]) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    config.output_dir.mkdir(parents=True, exist_ok=True)

    raw_path = config.output_dir / f"raw_{timestamp}.bin"
    raw_path.write_bytes(raw)

    commands_path = config.output_dir / f"commands_{timestamp}.txt"
    commands_path.write_text("\n".join(sent_commands) + "\n", encoding="utf-8")

    for encoding, text in decode_all(raw, config.preferred_encoding).items():
        decoded_path = config.output_dir / f"decoded_{timestamp}_{encoding}.txt"
        decoded_path.write_text(text, encoding="utf-8")

    print(f"Wrote raw log: {raw_path}")
    print(f"Wrote decoded logs to: {config.output_dir}")


def observe(config: ObservationConfig) -> None:
    started_at = time.monotonic()
    raw_log = bytearray()
    sent_commands: list[str] = []

    with socket.create_connection((config.host, config.port), timeout=READ_TIMEOUT_SECONDS) as sock:
        sock.settimeout(READ_TIMEOUT_SECONDS)
        raw_log.extend(read_available(sock, time.monotonic() + READ_TIMEOUT_SECONDS))

        for command in [config.name, config.password, *config.commands]:
            if time.monotonic() - started_at > MAX_SESSION_SECONDS:
                print("Session time limit reached; stopping observation.")
                break

            if sent_commands:
                time.sleep(MIN_COMMAND_INTERVAL_SECONDS)

            payload = (command + "\r\n").encode(config.preferred_encoding, errors="replace")
            sock.sendall(payload)
            sent_commands.append(command)
            raw_log.extend(read_available(sock, time.monotonic() + READ_TIMEOUT_SECONDS))

    write_logs(config, bytes(raw_log), sent_commands)


def main() -> None:
    args = build_parser().parse_args()
    config = ObservationConfig(
        host=args.host,
        port=args.port,
        name=args.name,
        password=args.password,
        commands=load_commands(args.commands_file),
        preferred_encoding=args.encoding,
        output_dir=args.output_dir,
    )
    observe(config)


if __name__ == "__main__":
    main()
