# SZData Schedule MCP Commands Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add explicit `schedule-mcp-*` CLI commands backed by the Data Portal schedule MCP and remove the partial direct schedule-runtime commands from the active `szdata` surface.

**Architecture:** Keep MCP transport in a small shared helper under `C:\Users\13246\.opencli\shared\szdata-core\commands\mcp\`. Add one command module per new `schedule-mcp-*` command under `commands\scheduling\`, with thin root wrappers under `C:\Users\13246\.opencli\clis\szdata\`. Retire the existing partial direct runtime wrappers from active `szdata` so users do not confuse them with MCP-equivalent commands.

**Tech Stack:** Node.js ES modules, `@jackwener/opencli/registry`, OpenCLI private adapter layout, MCP JSON-RPC over HTTP.

## Global Constraints

- Production `szdata` remains read-only.
- Do not output, record, or write API key, Bearer token, cookie, `X-Token`, or `X-Personal-Token` values.
- Read `X-Personal-Token` only from environment variables, preferably `SZDATA_X_PERSONAL_TOKEN`.
- Do not save GUIDs, complete DDL, complete SQL, or complete log bodies.
- Complete log bodies must not print by default; expose bounded previews and character counts.
- Use TDD: write failing tests before production code.
- Update workspace docs and `CHANGELOG.md` for material command changes.

---

### Task 1: MCP Client Helper

**Files:**
- Create: `C:\Users\13246\.opencli\shared\szdata-core\commands\mcp\mcp-client.js`
- Test: `C:\Users\13246\.opencli\shared\szdata-core\test\mcp-client.test.mjs`

**Interfaces:**
- Produces: `callMcpTool({ endpoint, tokenEnvNames, toolName, arguments: args, fetchImpl })`
- Produces: `resolvePersonalToken(env, names)`

- [ ] **Step 1: Write failing tests**

Test token resolution, missing token sanitization, initialize request, session id propagation, and tool result text parsing.

- [ ] **Step 2: Run test and verify RED**

Run:

```powershell
node --test C:\Users\13246\.opencli\shared\szdata-core\test\mcp-client.test.mjs
```

Expected: fails because `mcp-client.js` does not exist.

- [ ] **Step 3: Implement minimal helper**

Create a small fetch-based MCP JSON-RPC helper. Do not log headers or token values.

- [ ] **Step 4: Run test and verify GREEN**

Run the same `node --test` command and confirm pass.

### Task 2: Schedule MCP Command Modules

**Files:**
- Create: `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-dependencies.js`
- Create: `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-run-instances.js`
- Create: `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-run-states.js`
- Create: `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-run-logs.js`
- Create: `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-owner-failed-instances.js`
- Modify: `C:\Users\13246\.opencli\shared\szdata-core\test\schedule-commands.test.mjs`

**Interfaces:**
- Consumes: `callMcpTool(...)`
- Produces: OpenCLI command objects for the five new `schedule-mcp-*` commands.

- [ ] **Step 1: Write failing tests**

Add tests with mocked MCP callers that assert each command sends the correct tool name and arguments, normalizes the returned shape, marks `source: "mcp"`, and does not print full log content by default.

- [ ] **Step 2: Run tests and verify RED**

Run:

```powershell
node --test C:\Users\13246\.opencli\shared\szdata-core\test\schedule-commands.test.mjs
```

Expected: fails because new command modules do not exist.

- [ ] **Step 3: Implement command modules**

Use `Strategy.API`, `browser: false`, and `access: "read"` for MCP commands. Add a `--log-preview` bounded integer argument for `schedule-mcp-run-logs`.

- [ ] **Step 4: Run tests and verify GREEN**

Run the schedule test file again and confirm pass.

### Task 3: Register New Commands And Retire Partial Direct Runtime Wrappers

**Files:**
- Create root wrappers under `C:\Users\13246\.opencli\clis\szdata\schedule-mcp-*.js`
- Move active partial wrappers out of `C:\Users\13246\.opencli\clis\szdata\`
- Modify: `C:\Users\13246\.opencli\clis\szdata\COMMANDS.md`

**Interfaces:**
- Produces active CLI commands visible as `opencli szdata schedule-mcp-*`.

- [ ] **Step 1: Create thin wrappers**

Each wrapper imports the matching shared command, materializes it with `SZDATA_PROD`, and calls `cli(command)`.

- [ ] **Step 2: Retire old wrappers**

Move these active wrappers to an archive location after verifying paths:

```text
schedule-run-instances.js
schedule-run-states.js
schedule-run-logs.js
schedule-owner-failed-instances.js
```

Keep `schedule-dependencies.js` active only if it is still a direct schedule-detail utility; otherwise archive it too. User intent is to remove the half-baked MCP-like runtime commands.

- [ ] **Step 3: Update `COMMANDS.md`**

Document the new `schedule-mcp-*` commands and mark retired direct runtime commands as archived.

### Task 4: Workspace Docs

**Files:**
- Modify: `references/tools/szdata.md`
- Modify: `references/tools/szdata-command-landscape.md`
- Modify: `references/tools/szdata-operations/mcp-cli-function-comparison.md`
- Modify: `references/tools/szdata-operations/mcp-cli-coverage-report.md`
- Modify: `docs/superpowers/specs/2026-07-07-szdata-mcp-parity-cli-design.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces durable documentation that new agents can route to `schedule-mcp-*` for MCP-complete behavior.

- [ ] **Step 1: Update docs**

Replace wording that points users to partial direct runtime commands with the new `schedule-mcp-*` names.

- [ ] **Step 2: Run hygiene scans**

Run `git diff --check`, mojibake scan, and token/JWT/UUID-like scan over touched docs.

### Task 5: Verification

**Files:**
- Changed JavaScript files from Tasks 1-3.

- [ ] **Step 1: Syntax checks**

Run `node --check` on all changed `.js` files.

- [ ] **Step 2: Unit tests**

Run:

```powershell
node --test C:\Users\13246\.opencli\shared\szdata-core\test\mcp-client.test.mjs
node --test C:\Users\13246\.opencli\shared\szdata-core\test\schedule-commands.test.mjs
```

- [ ] **Step 3: CLI discovery**

Run:

```powershell
opencli szdata --help
```

Confirm `schedule-mcp-*` commands are visible and retired commands are no longer active.

- [ ] **Step 4: Bounded smoke**

If `SZDATA_X_PERSONAL_TOKEN` exists, run safe bounded MCP smokes:

```powershell
opencli szdata schedule-mcp-run-logs --task-id 238523 --data-date 2026-06-15 --log-preview 0 -f json
opencli szdata schedule-mcp-dependencies --task-id 238523 -f json
```

Do not print full log bodies or token values.
