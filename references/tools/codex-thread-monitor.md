# Codex Thread Monitor

This document defines how to use a main Codex thread to track other Codex conversations for this `Data-Engineering-Workbench` workspace.

It is not an OpenCLI adapter guide and does not describe platform business logic. It is a coordination note for keeping parallel Codex work understandable.

## Goal

Use one pinned main thread as the workspace coordinator. The coordinator should answer:

- Which Codex threads are currently working on this workspace?
- What has each thread finished?
- Which files, commands, or docs did each thread change?
- Which checks passed or failed?
- Which work is blocked or needs the user?
- Are two threads likely to conflict?

The coordinator should summarize progress. It should not take ownership of every task or duplicate the raw work of other agents.

## Current Dashboard

The lightweight dashboard lives at:

```text
tmp/codex-thread-dashboard.md
```

This file is a working snapshot, not a permanent source of business truth. Use it to coordinate active work, then promote stable findings into the relevant reference docs.

## When To Refresh

Refresh the dashboard when the user asks things like:

- "刷新看板"
- "看下其他 agent 进展"
- "这个目录下其他 Codex 做到哪了"
- "汇总一下 Data-Engineering-Workbench 里的对话"
- "有没有冲突/阻塞"

For manual refreshes, read recent same-workspace Codex threads, summarize only the latest useful turns, and update `tmp/codex-thread-dashboard.md`.

For recurring refreshes, use a thread automation only after the manual format is working well.

## What To Include

Each refresh should include:

- active threads and current goal
- completed threads and useful outputs
- changed files and generated docs
- verification commands and results
- blockers and user decisions needed
- cross-thread risks, especially overlapping adapter edits
- environment boundary risks, such as production write paths

Keep the summary short and operational. Avoid copying long prompts, raw JSON, SQL, stack traces, or terminal dumps unless the exact failure is needed.

## Evidence Boundaries

Thread summaries are coordination evidence. They are not automatically business facts.

For business or production conclusions:

- verify against current reference docs, live adapter source, current platform read-only data, or user confirmation
- distinguish production `szdata`, test `szdatatest`, local files, and inference
- do not treat historical `tmp/`, `_archive/`, or old thread messages as current source of truth without re-checking

## Thread Status Contract

Ask worker agents to include this block in milestone or final updates:

```text
## Thread Status
State: active / idle / blocked / done
Goal:
Done:
Changed files:
Verified:
Risks:
Next:
Need user:
```

This makes the coordinator more reliable and reduces guessing from partial conversation history.

## Coordinator Rules

- Filter to threads whose current working directory is `E:\02_area\agent-env\Data-Engineering-Workbench`.
- Default to recent turns only. Read older turns only when the latest status is unclear.
- Default to summaries, not full tool outputs.
- Do not expose secrets, cookies, tokens, internal connection strings, internal IPs, or ports.
- Do not steer, interrupt, hand off, archive, or rename other worker threads unless the user asks or there is a clear coordination need.
- If an active worker is editing `C:\Users\13246\.opencli\clis\szdata` or `C:\Users\13246\.opencli\clis\szdatatest`, flag possible adapter conflicts.
- If a worker reports production write, submit, delete, generate, preview, edit, or permission-changing actions, flag it unless explicit user authorization is visible.

## Recommended Cadence

Start with manual refreshes:

```text
刷新看板
```

If the format proves useful, schedule a thread automation every 15 or 30 minutes. The automation prompt should say:

```text
Refresh the Data-Engineering-Workbench Codex thread dashboard.
List same-workspace threads, read recent turns for active or recently updated threads, update tmp/codex-thread-dashboard.md, and report only important blockers, completed outputs, changed files, and cross-thread risks.
Do not copy raw tool output or sensitive details.
Stop or ask the user if repeated refreshes show no active work.
```

## What Not To Do

- Do not use this dashboard as a replacement for reference docs.
- Do not let multiple agents silently edit the same adapter files.
- Do not collapse role permission, topic base permission, application authorization, and current user runtime access into one flat permission claim.
- Do not assume `active` means progress; check recent turns and validation.
- Do not make this a heavy project-management system. It is a small coordination layer for parallel Codex work.
