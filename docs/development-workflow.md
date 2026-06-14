# 개발 흐름

이 프로젝트의 모든 의미 있는 변경은 브랜치와 Pull Request를 통해 진행합니다. Pull Request는 한국어로 작성하고, 코드 리뷰를 거친 뒤 `main`에 병합합니다.

## 브랜치

- `main`은 안정적인 통합 브랜치입니다.
- 파일을 수정하기 전에 짧게 사용할 작업 브랜치를 만듭니다.
- 브랜치 이름은 변경 목적이 드러나게 작성합니다.
  - `feature/<topic>`
  - `fix/<topic>`
  - `docs/<topic>`
  - `test/<topic>`

## 변경 절차

1. 깨끗한 `main`에서 시작합니다.
2. 작업 브랜치를 만듭니다.
3. 변경을 구현합니다.
4. 관련 검증 명령을 실행합니다.
5. 변경을 커밋합니다.
6. 브랜치를 원격 저장소에 푸시합니다.
7. `main`을 대상으로 Pull Request를 작성합니다.
8. Pull Request 제목과 본문은 한국어로 작성합니다.
9. Pull Request를 작성할 때 Copilot 리뷰를 요청합니다.
10. Copilot 리뷰가 완료되면 지적 사항을 검토합니다.
11. 필요한 수정 사항을 같은 PR 브랜치에 반영합니다.
12. Pull Request에 대한 코드 리뷰를 요청하고 리뷰 결과를 확인합니다.
13. 리뷰가 끝난 뒤에만 `main`에 병합합니다.
14. `main`으로 돌아와 워킹트리가 깨끗한지 확인합니다.

## 검증

일반적인 서버 변경에서는 다음 명령을 실행합니다.

```powershell
uv run python -m compileall exorcism_fortress tools
uv run python tools\smoke_test.py
uv run python tools\combat_smoke_test.py
uv run python tools\npc_interaction_smoke_test.py
```

변경 범위가 현재 스모크 테스트보다 크면 테스트를 추가합니다.

## Pull Request 작성

각 PR에는 다음 내용을 한국어로 포함합니다.

- 무엇을 변경했는지
- 왜 변경했는지
- 어떻게 검증했는지
- 남은 위험이나 후속 작업이 있는지

일반적인 프로젝트 변경에서 이 흐름을 건너뛰지 않습니다. 문서만 변경하는 경우에도 브랜치, 원격 Pull Request, 코드 리뷰, `main` 병합 절차를 따릅니다.

PR을 만들 때마다 Copilot 리뷰를 요청합니다. Copilot 리뷰가 완료되면 내용을 확인하고, 타당한 지적은 수정 커밋으로 반영한 뒤 병합합니다.
