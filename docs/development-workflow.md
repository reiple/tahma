# Development Workflow

This project uses a branch-and-PR workflow for every meaningful change. Pull Requests must be reviewed before they are merged into `main`.

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
6. Push the branch to the remote repository.
7. Open a Pull Request targeting `main`.
8. Review the Pull Request before merging.
9. Merge the PR into `main` only after review.
10. Return to `main` and confirm the working tree is clean.

## Verification

For normal server changes, run:

```powershell
uv run python -m compileall exorcism_fortress
uv run python tools\smoke_test.py
uv run python tools\combat_smoke_test.py
uv run python tools\npc_interaction_smoke_test.py
```

Add more tests when the changed behavior is larger than the current smoke test covers.

## Pull Request Notes

Each PR should include:

- What changed
- Why it changed
- How it was verified
- Any remaining risk or follow-up

Do not bypass this flow for normal project changes. Documentation-only changes still require a branch, remote Pull Request, review, and merge into `main`.

If no remote repository or PR tool is configured yet, keep the branch and commit history structured the same way. Once a remote is connected, push the branch and create the PR there before merging to `main`.
