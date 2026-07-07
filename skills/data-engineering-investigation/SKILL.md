---
name: data-engineering-investigation
description: Use for Data Engineering Workbench investigations that connect demand notes, local docs, code, wiki material, metadata, scheduling, SQL, and production facts into evidence-backed analysis without forcing a fixed workflow.
metadata:
  version: 0.1
  status: experimental
---

# Data Engineering Investigation

Use this skill when working in the Data Engineering Workbench or when a task
depends on its references, case notes, handoff material, or SZData/OpenCLI
operating rules.

## Entry Points

Read these first:

```text
AGENTS.md
CONTEXT.md
references/tools/opencli.md
references/tools/szdata.md
references/tools/szdata-operations/README.md
```

For Case Workbench design:

```text
references/tools/data-development-case-workbench.md
workbench-knowledge/README.md
workbench-knowledge/routes.md
```

For coordination across Codex conversations in this workspace:

```text
references/tools/codex-thread-monitor.md
tmp/codex-thread-dashboard.md
```

The dashboard path is local runtime state and is normally ignored by git.

## Environment Boundary

- `szdata` is production and is read-only by default.
- `szdatatest` is test and is the first validation surface for save, submit,
  preview, delete, generate, and edit-config actions.
- Production writes require passing `szdatatest` validation and explicit user
  authorization.
- For internal form workflows, success means downstream readback or follow-up
  page visibility, not just HTTP 200.

## Search Hygiene

- Use `rg` and `rg --files` first.
- Exclude `tmp/`, `_archive/`, `.headroom-cache/`, browser state, dependency
  folders, build outputs, and trace dumps unless the task explicitly targets
  them.
- Treat archived notes and historical traces as leads, not current truth.
- Verify current behavior against live adapter source or live read-only
  platform data when the answer depends on current state.

## Documentation Rule

When behavior, command semantics, adapter boundaries, or platform workflows
change, update the relevant durable docs:

```text
references/tools/opencli.md
references/tools/szdata.md
references/tools/szdata-operations/README.md
skills/data-engineering-investigation/SKILL.md
```
