from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exorcism_fortress.config import ServerConfig
from exorcism_fortress.server import MudServer


async def read_available(reader: asyncio.StreamReader) -> str:
    await asyncio.sleep(0.1)
    chunks: list[bytes] = []
    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=0.05)
        except TimeoutError:
            break
        if not chunk:
            break
        chunks.append(chunk)
        if len(chunk) < 4096:
            break
    return b"".join(chunks).decode("utf-8", errors="replace")


async def send_line(writer: asyncio.StreamWriter, text: str) -> None:
    writer.write((text + "\r\n").encode("utf-8"))
    await writer.drain()
    await asyncio.sleep(0.15)


async def main() -> None:
    config = ServerConfig(
        host="127.0.0.1",
        port=0,
        encoding="utf-8",
        command_cooldown_seconds=0.1,
        data_dir=Path("data"),
        save_dir=Path("saves"),
    )
    mud = MudServer(config)
    server = await asyncio.start_server(mud.handle_client, config.host, config.port)
    port = server.sockets[0].getsockname()[1]

    async with server:
        reader, writer = await asyncio.open_connection(config.host, port)
        output = await read_available(reader)
        await send_line(writer, "심리학과")
        output += await read_available(reader)
        await send_line(writer, "심리학과")
        output += await read_available(reader)
        await send_line(writer, "보기")
        output += await read_available(reader)
        await send_line(writer, "북")
        output += await read_available(reader)
        await send_line(writer, "종료")
        output += await read_available(reader)
        writer.close()
        await writer.wait_closed()

    expected = ["퇴마요새", "요새 정문", "중앙 마당"]
    missing = [text for text in expected if text not in output]
    if missing:
        raise AssertionError(f"missing expected text: {missing}\n{output}")
    print("SMOKE_TEST_OK")


if __name__ == "__main__":
    asyncio.run(main())
