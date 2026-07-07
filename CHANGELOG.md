# Changelog

## 2026-07-07 - agent change recording and push confirmation policy

### Changed
- Added explicit Agent rules requiring `CHANGELOG.md` updates for every material repository change.
- Added explicit Agent rules requiring user confirmation before any remote push.
- Clarified that edit or commit approval is not push approval.
- This round updates documentation and process contract only; it does not enter implementation.

### Files
- `AGENTS.md`
- `CHANGELOG.md`

### Decisions
- Keep the rule in root `AGENTS.md` because it is the first repository-level instruction file for future agents.
- Require pre-push summaries to include branch, commit id, changed files, verification performed, and changelog status.
- Require current-turn confirmation for each push, rather than relying on prior approval.

### Open Questions
- Whether to add a local pre-push hook later to mechanically block pushes without confirmation notes.
- Whether to add a reviewer checklist or CI rule for changelog coverage.

### Next
- Commit this rule change locally.
- Wait for user confirmation before pushing the commit to GitHub.

## 2026-07-07 - public repository bootstrap

### Changed
- Initialized the Data Engineering Workbench as a git-backed public documentation repository.
- Added public-facing repository entrypoints and security boundary notes.
- Added ignore rules for local runtime state, browser state, traces, archives, backups, caches, environment files, and scratch probes.
- Added line-ending normalization for text files.
- Published existing workbench references, case example material, dashboard design notes, skills, and workbench knowledge layer docs.
- Rewrote selected corrupted entrypoint docs into clean, agent-readable English.
- This round updated documentation, contracts, case examples, and repository structure only; it did not implement runtime application code.

### Files
- `.gitattributes`
- `.gitignore`
- `AGENTS.md`
- `CONTEXT.md`
- `README.md`
- `SECURITY.md`
- `.agents/skills/szdata-spec-first/SKILL.md`
- `skills/data-engineering-investigation/SKILL.md`
- `cases/CASE-20260611-jinshida-market-push/`
- `docs/dashboard-acceptance-checklist.md`
- `docs/dashboard-ui-spec.md`
- `docs/dashboard-view-model.md`
- `references/research/`
- `references/tools/`
- `workbench-knowledge/`

### Decisions
- Keep the repository public so cloud agents can read it directly.
- Keep local runtime state and raw transient artifacts out of git.
- Treat this repository as durable workbench documentation, not live adapter source.
- Keep production-oriented workflows read-only by default and require test-environment validation before state-changing operations.
- Prefer concise public entrypoints over copying local cache, browser state, or trace dumps.

### Open Questions
- Some historical Markdown files may still contain older wording or encoding issues outside the cleaned entrypoints.
- Public-safe abstraction depth may need tightening if future material contains more direct business data.
- The repository does not yet include automated linting for changelog coverage or secret scanning.

### Next
- Add a changelog gate so every future material change updates `CHANGELOG.md`.
- Review older reference files incrementally for encoding quality and public readability.
- Add lightweight checks for ignored runtime state and high-confidence secret patterns before future pushes.

## 2026-07-07 - changelog maintenance policy

### Changed
- Added root `CHANGELOG.md` as the required change record for future human and agent review.
- Added repository guidance that every document, schema, contract, Case example, or directory-structure change must update `CHANGELOG.md`.
- Added `CHANGELOG.md` to the main reader entrypoints.
- This round updates documentation and process contract only; it does not enter implementation.

### Files
- `CHANGELOG.md`
- `AGENTS.md`
- `README.md`

### Decisions
- Changelog entries must be concise and record only real changes.
- Every entry must include date, phase, changed summary, files, decisions, open questions, and next steps.
- Sensitive internal details, real accounts, cookies, tokens, and production connection details must not be recorded.
- Reviewer should treat missing changelog updates for obvious file changes as an incomplete delivery.

### Open Questions
- Whether to add an automated changelog coverage check later.
- Whether to split future changelog entries by Case, tool surface, or release-style phase when changes grow larger.

### Next
- Keep `CHANGELOG.md` updated in the same commit as future material changes.
- Consider a small reviewer checklist or CI check once the repository has more regular updates.
