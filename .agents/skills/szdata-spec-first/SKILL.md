---
name: szdata-spec-first
description: Use before changing or reviewing szdata/szdatatest dataset, dataset-config, dataset-create-columns, dataset-create, wide-table, or widetable OpenCLI adapters; enforces spec-first review, environment boundaries, output-column parsing, usageType 3/5 wide-table lifecycle rules, and readback verification.
---

# SZData Spec First

Use this skill before modifying or reviewing `szdata` / `szdatatest` OpenCLI
adapters related to dataset management or wide-table management.

## Required References

Read the relevant specs first:

- `references/tools/szdata-operations/specs/dataset-save-flow.md`
- `references/tools/szdata-operations/specs/wide-table-lifecycle.md`

Then read the usual workspace references when behavior or docs may change:

- `references/tools/opencli.md`
- `references/tools/szdata.md`
- `references/tools/szdata-operations/README.md`
- `references/tools/szdata-operations/dataset-create.md`
- `references/tools/szdata-operations/wide-table-management.md`

## Workflow

1. Identify whether the task is read-only review, ordinary dataset save,
   output-column parsing, wide-table save/preview/generation, or production
   write planning.
2. Restate the applicable spec boundary before editing.
3. Inspect live adapter source under:
   - `C:\Users\13246\.opencli\clis\szdata`
   - `C:\Users\13246\.opencli\clis\szdatatest`
4. For SQL dataset save behavior, verify that `获取输出列` is represented by
   `dataset-create-columns` and that save mode cannot use `--fields-file` as a
   substitute for parsed output columns.
5. For usageType `3`/`5`, keep ordinary `dataset-create --save` blocked. Use
   explicit wide-table lifecycle commands for config save, preview, generation,
   upgrade, offline, or delete.
6. Keep `szdata` production read-only unless the user explicitly authorizes the
   exact production write after `szdatatest` validation.
7. After adapter edits, run `node --check` on changed JavaScript and at least one
   dry-run or read-only smoke test. Run platform writes only when the user has
   authorized that specific test action.
8. Update specs or references when behavior, command semantics, endpoints, or
   validation rules change.

## Chrome UI Recon To OpenCLI

When a workflow depends on a real platform form or button state, use the Codex
Chrome Extension to inspect the live page before trusting an adapter. Read DOM
validation errors, current route parameters, visible form values, and relevant
network behavior, then compare that UI evidence with OpenCLI readback. Only
after this UI-to-API reconciliation should the behavior be encoded as an
OpenCLI adapter.

For wide-table schedule configuration, do not inspect only the red validation
boxes. Compare the full DispatchTaskConfig point list: visible required fields,
visible optional fields, mounted-hidden extension fields, option dictionaries,
db/table consistency, SQL/pre-SQL/post-SQL presence, engine/source settings,
retry settings, concurrency, and partition file count. A stale Chrome tab can
show first-time blank required fields even when `widetable-schedule-config` and
`widetable-schedule-detail` read back a populated task; refresh or reopen the
route before treating UI errors as platform truth.

## OpenCLI Help Usage

- Use `--help` for command discovery and argument confirmation only.
- Do not treat full `--help` output as behavior verification.
- During reviews, filter help output for key command names or flags instead of
  loading the full text when possible.
- Verify behavior with bounded `-f json` dry-runs, read-only self-checks, and
  downstream readback.

## Hard Rules

- Do not hide wide-table lifecycle writes behind ordinary dataset commands.
- Do not save SQL datasets without fresh output-column parsing.
- Do not treat HTTP 200 as success for form workflows; read downstream state.
- Do not print tokens, cookies, internal hosts, internal IPs, ports, or gateway
  details in final summaries.
- Do not add production write commands without clear naming, dry-run defaults,
  confirmation flags, and explicit user authorization.
