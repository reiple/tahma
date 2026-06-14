# Development Workflow

This project uses a branch-and-PR workflow for every meaningful change.

## Branches

- `main` is the stable integration branch.
- Create a short-lived branch before changing files.
- Use branch names that describe the purpose:
  - `feature/<topic>`
  - `fix/<topic>`
  - `docs/<topic>`
  - `test/<topic>`

## Change Flow

1. Start from a clean `main`.
2. Create a branch.
3. Make the change.
4. Run the relevant verification commands.
5. Commit the change.
6. Open a Pull Request targeting `main`.
7. Merge the PR after review.
8. Return to `main` and confirm the working tree is clean.

## Verification

For normal server changes, run:

```powershell
uv run python -m compileall exorcism_fortress
uv run python tools\smoke_test.py
uv run python tools\combat_smoke_test.py
```

Add more tests when the changed behavior is larger than the current smoke test covers.

## Pull Request Notes

Each PR should include:

- What changed
- Why it changed
- How it was verified
- Any remaining risk or follow-up

If no remote repository or PR tool is configured yet, keep the branch and commit history structured the same way. Once a remote is connected, push the branch and create the PR there before merging to `main`.
