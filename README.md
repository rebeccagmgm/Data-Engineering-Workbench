# Data Engineering Workbench

This repository is a public, agent-readable workbench for data-engineering
investigation patterns, local operating rules, case notes, and reusable
handoff material.

It is not the live OpenCLI adapter source tree. The files here explain how an
agent should reason about the work; they do not replace the private adapter
code or the live business systems.

## Start Here

- `AGENTS.md`: project rules, environment boundaries, search hygiene, and
  documentation rules.
- `CONTEXT.md`: the shared language for the Case Workbench model.
- `skills/data-engineering-investigation/SKILL.md`: compact skill entrypoint
  for agents.
- `references/tools/`: tool and platform reference notes.
- `references/tools/szdata-operations/README.md`: operation-specific SZData
  documentation.
- `workbench-knowledge/README.md`: reusable case templates, workflow patterns,
  capability contracts, and promotion rules.
- `cases/`: bounded example cases and historical replay notes.

## Repository Boundary

The repository is intended for public reading by cloud agents. It should keep
durable, reusable material and exclude local runtime state.

Ignored by default:

- `tmp/`
- `_archive/`
- `.headroom-cache/`
- `backups/`
- `_browser_state.txt`
- `*.trace`
- `.env*`

Do not add cookies, tokens, private keys, raw browser state, full trace dumps,
or unbounded production payloads.

## Environment Rules

- `szdata` refers to the production data platform and is read-only by default.
- `szdatatest` refers to the test data platform and is the validation surface
  for save, submit, preview, delete, generate, and edit-config actions.
- Production writes require a passing test-environment validation and explicit
  user authorization.
- For form workflows, success means the downstream or follow-up page can read
  the result, not merely that an API returned HTTP 200.

## How Agents Should Use This Repo

1. Read `AGENTS.md`.
2. Read `CONTEXT.md` for terminology.
3. Use `references/tools/opencli.md` and `references/tools/szdata.md` before
   working on OpenCLI or SZData tasks.
4. Use operation-specific docs under `references/tools/szdata-operations/`
   before touching dataset or wide-table workflows.
5. Treat case evidence as historical unless current live readback confirms it.
