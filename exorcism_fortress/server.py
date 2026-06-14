from __future__ import annotations

import asyncio
import logging
import time
from contextlib import suppress

from .commands import execute_command
from .config import SUPPORTED_ENCODINGS, ServerConfig
from .encoding import decode_client_line, encode_server_text
from .models import Player
from .storage import PlayerStore
from .world import World

PROMPT = "\r\n> "


class MudServer:
    def __init__(self, config: ServerConfig) -> None:
        self.config = config
        self.world = World.load(config.data_dir)
        self.players = PlayerStore(config.save_dir)
        self.sessions: set[ClientSession] = set()

    async def start(self) -> None:
        self.config.log_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=self.config.log_dir / "server.log",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            encoding="utf-8",
        )
        server = await asyncio.start_server(self.handle_client, self.config.host, self.config.port)
        sockets = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
        print(f"퇴마요새 서버가 시작되었습니다: {sockets}")
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        session = ClientSession(self, reader, writer)
        self.sessions.add(session)
        try:
            await session.run()
        except ConnectionError:
            pass
        except Exception:
            logging.exception("client session failed")
        finally:
            self.sessions.discard(session)
            await session.close()

    async def broadcast(self, message: str, sender: "ClientSession") -> None:
        for session in tuple(self.sessions):
            if session is sender or session.player is None:
                continue
            await session.send("\r\n" + message + PROMPT)


class ClientSession:
    def __init__(self, server: MudServer, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.server = server
        self.reader = reader
        self.writer = writer
        self.encoding = server.config.encoding
        self.player: Player | None = None
        self.last_command_at = 0.0

    async def run(self) -> None:
        await self.send("퇴마요새에 접속했습니다.\r\n한글이 깨지면 다른 터미널 인코딩을 시도하세요.\r\n\r\n이름: ")
        name = await self.read_line()
        await self.send("암호: ")
        password = await self.read_line()

        player, message = self.server.players.load(name.strip(), password.strip())
        if player is None:
            await self.send((message or "로그인할 수 없습니다.") + "\r\n")
            return

        self.player = player
        logging.info("player logged in: %s", player.name)
        await self.send(f"\r\n{message}\r\n")
        await self.send(self.server.world.describe_room(player.room_id) + PROMPT)

        while True:
            raw_line = await self.read_line()
            now = time.monotonic()
            elapsed = now - self.last_command_at
            if elapsed < self.server.config.command_cooldown_seconds:
                wait = self.server.config.command_cooldown_seconds - elapsed
                await self.send(f"명령은 천천히 입력해야 합니다. {wait:.1f}초 뒤에 다시 시도하세요." + PROMPT)
                continue
            self.last_command_at = now

            if await self.try_change_encoding(raw_line):
                continue

            result = execute_command(raw_line, player, self.server.world)
            if result.message:
                await self.send(result.message + PROMPT)
            else:
                await self.send(PROMPT)
            if result.broadcast:
                await self.server.broadcast(result.broadcast, self)
            self.server.players.save(player)
            if result.should_quit:
                return

    async def try_change_encoding(self, raw_line: str) -> bool:
        command, _, value = raw_line.strip().partition(" ")
        if command.lower() not in {"인코딩", "encoding"}:
            return False
        encoding = value.strip().lower()
        if encoding not in SUPPORTED_ENCODINGS:
            await self.send("지원 인코딩: " + ", ".join(SUPPORTED_ENCODINGS) + PROMPT)
            return True
        self.encoding = encoding
        await self.send(f"현재 접속 인코딩을 {encoding}(으)로 변경했습니다." + PROMPT)
        return True

    async def read_line(self) -> str:
        data = await self.reader.readline()
        if not data:
            raise ConnectionError("client disconnected")
        line, detected_encoding = decode_client_line(data, self.encoding)
        if detected_encoding != self.encoding:
            self.encoding = detected_encoding
        return line

    async def send(self, text: str) -> None:
        self.writer.write(encode_server_text(text, self.encoding))
        await self.writer.drain()

    async def close(self) -> None:
        if self.player is not None:
            self.server.players.save(self.player)
        self.writer.close()
        with suppress(Exception):
            await self.writer.wait_closed()
