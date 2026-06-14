from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .config import SUPPORTED_ENCODINGS, ServerConfig
from .server import MudServer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="퇴마요새 Python 텍스트 MUD 서버")
    parser.add_argument("--host", default="127.0.0.1", help="서버 바인딩 주소")
    parser.add_argument("--port", type=int, default=6666, help="서버 포트")
    parser.add_argument("--encoding", choices=SUPPORTED_ENCODINGS, default="utf-8", help="기본 클라이언트 인코딩")
    parser.add_argument("--cooldown", type=float, default=1.0, help="플레이어별 명령 입력 제한 초")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="월드 데이터 디렉터리")
    parser.add_argument("--save-dir", type=Path, default=Path("saves"), help="플레이어 저장 디렉터리")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = ServerConfig(
        host=args.host,
        port=args.port,
        encoding=args.encoding,
        command_cooldown_seconds=args.cooldown,
        data_dir=args.data_dir,
        save_dir=args.save_dir,
    )
    try:
        asyncio.run(MudServer(config).start())
    except KeyboardInterrupt:
        print("\n퇴마요새 서버를 종료합니다.")


if __name__ == "__main__":
    main()
