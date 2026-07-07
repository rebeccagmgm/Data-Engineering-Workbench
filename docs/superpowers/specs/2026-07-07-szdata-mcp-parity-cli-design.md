# SZData Schedule MCP CLI Design

Status: Implemented direction
Date: 2026-07-07

## Goal

Expose the Data Portal schedule MCP tools as explicit `szdata` CLI commands and remove the previous partial direct runtime commands from the active `szdata` surface.

The new active commands are:

- `schedule-mcp-dependencies`
- `schedule-mcp-run-instances`
- `schedule-mcp-run-states`
- `schedule-mcp-run-logs`
- `schedule-mcp-owner-failed-instances`

## Background

Current investigation showed that the old direct schedule runtime commands were useful as Portal probes, but not MCP-equivalent:

- dependencies only parsed upstream `tasklink`
- run states were derived from instance lists
- run logs did not expose full MCP log fields
- owner failed instances used a Portal worklist view

The user chose a simpler final direction: wrap MCP directly for this schedule subset and stop presenting the partial direct commands as active MCP-like CLI tools.

## Non-Goals

- Do not continue hard-reconstructing a non-MCP direct API for these schedule MCP tools in this phase.
- Do not print or store API keys, Bearer tokens, cookies, `X-Token`, or `X-Personal-Token` values.
- Do not save GUIDs, complete DDL, complete SQL, or complete log bodies.
- Do not execute production writes.
- Do not hide MCP usage behind old command names.

## User-Facing Design

Use explicit MCP-backed command names:

```text
schedule-mcp-dependencies
schedule-mcp-run-instances
schedule-mcp-run-states
schedule-mcp-run-logs
schedule-mcp-owner-failed-instances
```

The old active wrappers are retired:

```text
schedule-dependencies
schedule-run-instances
schedule-run-states
schedule-run-logs
schedule-owner-failed-instances
```

They may remain in archive or shared implementation history, but should not be exposed as active `opencli szdata` choices.

## Authentication

The MCP commands call:

```text
https://data.gf.com.cn/mcp/schedule
```

They read `X-Personal-Token` only from environment variables. Preferred variable:

```text
SZDATA_X_PERSONAL_TOKEN
```

Errors may name missing environment variables, but must never print token values.

## Output Rules

Every new MCP-backed command should identify its source:

- `source`: `mcp`
- `evidenceLevel`: the MCP tool evidence, for example `mcp_schedule_get_task_run_logs`
- `parityLevel`: currently `mcp_shape_compatible`

For `schedule-mcp-run-logs`, complete log bodies are not printed by default. The command returns:

- log availability
- bad/full log character counts
- bounded previews controlled by `--log-preview`

Default `--log-preview 0` hides log bodies.

## Implementation Shape

Shared MCP transport:

```text
C:\Users\13246\.opencli\shared\szdata-core\commands\mcp\mcp-client.js
```

Shared schedule MCP helpers:

```text
C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-service.js
```

Command modules:

```text
C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-dependencies.js
C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-run-instances.js
C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-run-states.js
C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-run-logs.js
C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-owner-failed-instances.js
```

Root wrappers:

```text
C:\Users\13246\.opencli\clis\szdata\schedule-mcp-dependencies.js
C:\Users\13246\.opencli\clis\szdata\schedule-mcp-run-instances.js
C:\Users\13246\.opencli\clis\szdata\schedule-mcp-run-states.js
C:\Users\13246\.opencli\clis\szdata\schedule-mcp-run-logs.js
C:\Users\13246\.opencli\clis\szdata\schedule-mcp-owner-failed-instances.js
```

Archived wrappers:

```text
C:\Users\13246\.opencli\archive\clis\szdata\20260707-mcp-replaced\
```

## Testing And Verification

Unit tests:

```powershell
node --test C:\Users\13246\.opencli\shared\szdata-core\test\mcp-client.test.mjs
node --test C:\Users\13246\.opencli\shared\szdata-core\test\schedule-commands.test.mjs
```

Syntax checks:

```powershell
node --check <changed-js-file>
```

CLI discovery:

```powershell
opencli szdata --help
```

MCP smoke tests may run only when `SZDATA_X_PERSONAL_TOKEN` is present. Keep them bounded and do not print full logs.

## Acceptance Criteria

- Active `szdata` exposes the five `schedule-mcp-*` commands.
- Active `szdata` no longer exposes the five old partial direct runtime wrappers.
- MCP commands do not require Chrome/browser session.
- Missing token errors are sanitized.
- Full log bodies are not emitted by default.
- Docs and changelog reflect the command replacement.
