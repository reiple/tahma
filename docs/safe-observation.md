# Safe Observation Guide

The existing MUD server is a live service. Treat observation as a slow, manual, low-impact activity.

## Rules

- Use one connection at a time.
- Keep each session short.
- Keep command files small: at most 8 commands.
- The observation tool waits at least 1.5 seconds between commands.
- Do not use generated map crawlers or brute-force command discovery.
- Avoid repeating state-changing commands.
- Stop immediately if the server becomes slow or returns unexpected errors.

## Command File

Create a UTF-8 text file with one command per line. Empty lines and lines beginning with `#` are ignored.

Example:

```text
# Keep this deliberately short.
도움말
보기
소지품
종료
```

## Run

```powershell
uv run python tools\observe_existing_server.py --commands-file work\observe_commands.txt --encoding cp949
```

The tool stores:

- Raw bytes: `logs/observations/raw_*.bin`
- Commands sent: `logs/observations/commands_*.txt`
- Decoded text variants: `logs/observations/decoded_*_utf-8.txt`, `*_cp949.txt`, `*_euc-kr.txt`

Observation logs are runtime artifacts and are intentionally ignored by Git.
