# 퇴마요새 / Exorcism Fortress

Python 3.12와 uv로 실행하는 한국어 텍스트 MUD 서버입니다.

## 현재 가능한 것

- `uv` 기반 Python 3.12 가상환경 실행
- TCP/Telnet 클라이언트 접속
- 한국어 입출력
- `utf-8`, `cp949`, `euc-kr` 인코딩 선택
- Telnet 제어 바이트 기본 제거
- 플레이어별 명령 입력 쿨다운
- 이름/암호 로그인
- 플레이어 위치, 체력, 경험치, 소지품, 장비 저장
- JSON 기반 방, 아이템, NPC 데이터 로딩
- 방 설명 표시와 방향 이동
- 기존 서버 관찰 기반 장소명 이동
- 아이템 줍기/버리기
- NPC 살피기와 대화
- 기본 전투
- `입장티켓` 수령 흐름
- `모두 무장`으로 엑토스탭 착용
- 기존 운영 서버 저부하 관찰 도구
- 기본/전투/NPC 상호작용 스모크 테스트

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
- `광장`
- `북`, `남`, `동`, `서`
- `소지품`
- `줍기 <물건>`
- `버리기 <물건>`
- `살피기 <대상>`
- `대화 <대상>`
- `상태`
- `휴식`
- `공격 <대상>`
- `입장티켓`
- `모두 무장`
- `말 <내용>`
- `인코딩 utf-8`, `인코딩 cp949`, `인코딩 euc-kr`
- `종료`

## 관찰 반영 동선

기존 서버 관찰 결과를 바탕으로 시작 지역은 `대기실 -> 광장 -> 서 -> 서 -> 입장티켓 -> 동 -> 동 -> 북 -> 나가는길 -> 모두 무장 -> 광장 -> 남` 흐름을 우선 반영했습니다.

현재 반영된 주요 장소:

- `대기실`
- `광장`
- `광장` 서쪽
- `공공건물1층`
- `광장` 북쪽
- `상가`
- `봉인 제단`

현재 반영된 주요 NPC/대상:

- `연희`
- `공지맨`
- `네스포린`
- `흔들리는 그림자`
- `종이 부적`
- `입장티켓`
- `축복받은 엑토스탭`

관찰 당시 `나가는길`은 사용자 상태 기준으로 `상가`로 이동하는 것으로 확인되어 그 동작을 우선 반영했습니다.

## 검증

```powershell
uv run python -m compileall exorcism_fortress tools
uv run python tools\smoke_test.py
uv run python tools\combat_smoke_test.py
uv run python tools\npc_interaction_smoke_test.py
```

## 개발 흐름

모든 수정 사항은 새 브랜치에서 작업하고 원격 저장소에 Pull Request를 작성합니다. Pull Request는 코드 리뷰를 거친 뒤 `main`에 반영합니다.

## 운영 서버 분석 원칙

기존 운영 서버를 참고할 때는 자동 명령 반복을 피하고, 명령 사이에 최소 1초 이상 대기합니다. 이 프로젝트의 서버도 기본적으로 플레이어별 1초 명령 쿨다운을 적용합니다.

자세한 관찰 절차와 저부하 관찰 도구 사용법은 `docs/safe-observation.md`를 참고하세요.
