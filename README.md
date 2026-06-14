# 퇴마요새 / Exorcism Fortress

Python 3.12와 uv로 실행하는 한국어 텍스트 MUD 서버입니다.

## 실행

```powershell
uv run python main.py --host 127.0.0.1 --port 6666
```

다른 터미널에서 접속합니다.

```powershell
telnet 127.0.0.1 6666
```

Windows에서 telnet이 없으면 PuTTY, Tera Term, nc 같은 TCP 클라이언트를 사용하면 됩니다.

## 주요 옵션

```powershell
uv run python main.py --encoding cp949 --cooldown 1.0
```

- `--encoding`: `utf-8`, `cp949`, `euc-kr`
- `--cooldown`: 명령 입력 간 최소 대기 시간입니다.
- `--data-dir`: `rooms.json`, `items.json` 위치입니다.
- `--save-dir`: 플레이어 저장 위치입니다.

## 기본 명령어

- `도움말`
- `보기`
- `북`, `남`, `동`, `서`
- `소지품`
- `줍기 <물건>`
- `버리기 <물건>`
- `상태`
- `휴식`
- `공격 <대상>`
- `말 <내용>`
- `인코딩 utf-8`, `인코딩 cp949`, `인코딩 euc-kr`
- `종료`

## 운영 서버 분석 원칙

기존 운영 서버를 참고할 때는 자동 명령 반복을 피하고, 명령 사이에 최소 1초 이상 대기합니다. 이 프로젝트의 서버도 기본적으로 플레이어별 1초 명령 쿨다운을 적용합니다.

자세한 관찰 절차와 저부하 관찰 도구 사용법은 `docs/safe-observation.md`를 참고하세요.
