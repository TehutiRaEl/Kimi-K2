# Kimi-K2 — Governance

Kimi-K2 is the Mind colony (archetype: mind/language gateway) of the
Sovereign Hive federation. This file is a short, colony-local pointer into
the federation-wide governance convention defined in
[TehutiRaEl/THEHIVE](https://github.com/TehutiRaEl/THEHIVE/blob/claude/session-continuation-owj5wr/docs/GOVERNANCE.md).

## Principles

Contributions here favor reviewable, single-purpose commits; no destructive
operation (deleting data, force-pushing, dropping schema) happens without
explicit human confirmation; and any change that affects the colony's
public `/colony/*` contract or cross-repo behavior gets a human reviewer
before merge, in line with the federation-wide principles in THEHIVE's
`docs/GOVERNANCE.md`.

## Relevant Roles

The full 101-role catalog lives in
[THEHIVE/docs/ROLES.md](https://github.com/TehutiRaEl/THEHIVE/blob/claude/session-continuation-owj5wr/docs/ROLES.md).
Roles most relevant to this repo:

| # | Role Title | Responsibility |
|---|---|---|
| 12 | Mind Colony Director | Owns Kimi-K2's language-model gateway roadmap. |
| 27 | Language Model Gateway Lead | Owns model routing and fallback conventions. |
| 62 | Model Gateway Architect | Owns model-routing architecture. |
| 68 | Backend Engineer (Kimi-K2) | Implements model-gateway route features. |
| 74 | Database Engineer (NAR2, 4DBRAIN, Kimi-K2) | Implements local persistence layers. |
| 76 | Test Engineer (NAR2, 4DBRAIN, Kimi-K2) | Writes/maintains colony test coverage. |
| 87 | Code Reviewer Apprentice (Kimi-K2) | Performs first-pass PR review. |
| 99 | Artifact Cleanup (THEHIVE, NAR2, 4DBRAIN, Kimi-K2) | Removes stale cache/build artifacts from version control. |

## Commit / PR Convention

```
[ROLE: <Role Title>] type(scope): description

Rationale: <one sentence on why this change is needed>
```

`type` follows Conventional Commits (`feat`/`fix`/`docs`/`chore`/`refactor`/`test`).

## Enforcement

Advisory only — see `.github/workflows/governance-check.yml`. It never
fails the build and is not a required status check.
